from dataclasses import dataclass
from typing import ByteString
from typing import Tuple


async def sig_cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:
    ...


@dataclass
class CacheTarget:
    path: str
    value: bytes

    def __bool__(self):
        return bool(self.value)

    def __iter__(self):
        yield self.path
        yield self.value


async def post_cache(hub, ctx):
    # Validate the return
    if not ctx.ret:
        return CacheTarget("", b"")
    path, value = ctx.ret
    return CacheTarget(path, value)
