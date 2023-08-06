"""
This module is used to retrieve files from a local source
"""
import mimetypes
import os
import pathlib
from typing import ByteString
from typing import Tuple

__virtualname__ = "file"


async def process(
    hub, ctx, protocol: str, source_path: str, loc: str
) -> Tuple[str, ByteString]:
    """
    Determine if a file has mimetypes, if so, unravel it and save it's tree in memory
    """
    filemimetypes = mimetypes.guess_type(source_path)
    if all(elem is None for elem in filemimetypes):
        file_extension = pathlib.Path(source_path).suffix
        if file_extension:
            filemimetypes = file_extension, None
    if filemimetypes:
        for plugin in hub.source:
            if not hasattr(plugin, "MIMETYPE"):
                continue
            if plugin.MIMETYPE in filemimetypes:
                return await plugin.cache(
                    ctx=ctx, protocol=protocol, source=source_path, location=loc
                )


async def cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:
    """
    Take a file from a location definition and cache it in memory
    """
    # Check if the file has a mimetype and call the right plugin
    source_path = source

    if os.path.isfile(source_path):
        ref, mime_source = await hub.source.file.process(
            ctx, protocol, source_path, location
        )
        if mime_source:
            return ref, mime_source

    # No mimetypes, read a plain SLS file
    full = os.path.join(source_path, location)
    if os.path.isfile(full):
        with open(full, "rb") as rfh:
            in_memory_file = rfh.read()

        return full, in_memory_file
