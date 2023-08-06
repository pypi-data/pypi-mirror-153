import io
import tarfile
from pathlib import Path
from typing import ByteString
from typing import Tuple

import msgpack
from cryptography.fernet import Fernet

MIMETYPE = ".epkg"

"""
Process encrypted archive source
"""


def __init__(hub):
    hub.source.file.ACCT = ["file"]


async def cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:
    # name of epkg and key name (to decrypt the package) should match
    key = Path(source).stem
    f = Fernet(ctx.acct.get(key))
    with open(source, "rb") as rfh:
        data = msgpack.loads(rfh.read())
        decrypted_data = f.decrypt(data["token"])
        raw = io.BytesIO(decrypted_data)
        with tarfile.open(fileobj=raw, mode="r:xz") as tar:
            members = tar.getmembers()
            for member in members:
                if member.name.endswith(location):
                    location = member.name
                    break
            file = tar.extractfile(location)
            if file:
                return location, file.read()
