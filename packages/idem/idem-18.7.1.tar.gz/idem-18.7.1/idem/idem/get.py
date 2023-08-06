"""
This file contains routines to get sls files from references
"""
import re
from typing import ByteString
from typing import List
from typing import Tuple

SOURCE_PATTERN = re.compile(r"^((\w+)(?:\+\w+)*)://(?:(.*)@)?(.+)$")


def parse_source(hub, source: str) -> Tuple[str, str, str, str]:
    match = SOURCE_PATTERN.match(source)
    if not match:
        raise ValueError(f"SLS source is not a valid pattern: {source}")
    protocol = match.group(1)
    protocol_plugin = match.group(2)
    acct_profile = match.group(3)
    data = match.group(4)
    return protocol, protocol_plugin, acct_profile, data


async def ref(hub, name: str, sls: str, sources: List[str]) -> Tuple[str, ByteString]:
    """
    Cache the given file from the named reference point

    :param hub:
    :param name: The state run name
    :param sls: an SLS location within the given sources
    :param sources: sls-sources or params-sources

    :returns A file_name/identifier and encoded yaml content

    If the sls sources uses `acct` for authentication, then a profile is specified as part of the sls_source

    .. code-block::

        [proto]://[acct_profile]@[path]
    """
    acct_data = hub.idem.RUNS[name]["acct_data"]

    for source in sources:
        protocol, protocol_plugin, acct_profile, data = hub.idem.get.parse_source(
            source
        )
        if not acct_profile:
            acct_profile = "default"
        path = sls.replace(".", "/")
        locations = [f"{path}.sls", f"{path}/init.sls", path]

        ctx = await hub.idem.acct.ctx(
            protocol_plugin,
            acct_profile=acct_profile,
            acct_data=acct_data,
        )

        for location in locations:
            processed_location, encoded_yaml_content = await hub.source[
                protocol_plugin
            ].cache(ctx, protocol=protocol, source=data, location=location)
            if encoded_yaml_content:
                return processed_location, encoded_yaml_content
    else:
        raise LookupError(f"Could not find SLS ref {sls} in sources")
