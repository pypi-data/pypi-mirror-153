from typing import Any
from typing import Dict

import pop.contract


def client(hub, path: str, context):
    """
    Get an Vault client based on the path and call an operation on it
    idem will automatically populate credentials from acct in the client.

    The calls mirror the namespacing of hvac.Client and have the same parameters

    path::

        hvac.client.[service_path].[operation] [kwargs="values"]

    Examples:
        In these examples will use the service_path "secrets.kv.v2" and operation of "read_secret_version"

        Call from the CLI
        .. code-block: bash

            $ idem exec hvac.client.secrets.kv.v2.read_secret_version path="secret/test"

        Call from code
        .. code-block: python

            await hub.exec.hvac.client.secrets.kv.v2.read_secret_version(ctx, path="secret/test")

    :param hub:
    :param path: client.[service_path].[function_name]
    :param context: None
    :return: The result of the call
    """
    path_list = path.split(".")
    assert len(path_list) > 2
    c = path_list[0]
    service_path = path_list[1:-1]
    operation = path_list[-1]
    assert c == "client"

    async def _client_caller(ctx, *args, **kwargs) -> Dict[str, Any]:
        result = {"comment": (), "ret": None, "result": True}
        try:
            ret: Dict[str, Any] = await hub.tool.hvac.client.exec(
                ctx=ctx, service_path=service_path, operation=operation, *args, **kwargs
            )
            if hasattr(ret, "keys"):
                keys = sorted(ret.keys())
            else:
                keys = []
            result["comment"] = tuple(keys)
            result["ret"] = ret
            result["result"] = bool(ret)
        except Exception as e:
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
        return result

    return pop.contract.ContractedAsync(
        hub,
        contracts=[],
        func=_client_caller,
        ref=path,
        name=operation,
        implicit_hub=False,
    )
