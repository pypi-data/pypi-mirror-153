"""
Process zip source
"""
import zipfile
from typing import ByteString
from typing import Tuple

__virtualname__ = "zip"

MIMETYPE = "application/zip"


async def cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:

    if zipfile.is_zipfile(source):
        zip_source = zipfile.ZipFile(source)

        # Store the contents of the zip file in memory
        return location, zip_source.read(location)
