import json
from typing import ByteString
from typing import Tuple

__virtualname__ = "vault"


def __init__(hub):
    hub.source.vault.ACCT = ["vault"]


async def cache(
    hub, ctx, protocol: str, source: str, location: str
) -> Tuple[str, ByteString]:
    # Location ends with .sls
    if location.endswith(".sls"):
        location = location[:-4]

    if location != source:
        # This source wasn't specified with --params
        return "", b""

    version = ctx.acct.get("version", "v2")
    if version == "v1":
        data: bytes = await hub.exec.hvac.client.secrets.kv.v1.read_secret(
            ctx=ctx, path=location
        )
        return_data = (
            json.dumps(data["ret"].get("data")).encode("utf-8")
            if data["result"] and data["ret"]
            else None
        )
        return "", return_data
    else:
        data: bytes = await hub.exec.hvac.client.secrets.kv.v2.read_secret_version(
            ctx=ctx, path=location
        )
        return_data = (
            json.dumps(data["ret"].get("data").get("data")).encode("utf-8")
            if data["result"] and data["ret"] and data["ret"].get("data")
            else None
        )
        return "", return_data
