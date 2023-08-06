from typing import Any
from typing import Dict
from typing import List

import hvac

ITERATION_FINISHED = object()

__func_alias__ = {"exec_": "exec"}


async def exec_(
    hub,
    ctx,
    service_path: List,
    operation: str,
    *op_args,
    **op_kwargs: Dict[str, Any],
) -> Any:
    """
    :param hub:
    :param ctx:
    :param service_path: The name of the service client to create
    :param operation: The operation to run from the service client
    :param op_args: arguments to pass to the operation call
    :param op_kwargs: keyword arguments to pass to the operation call

    :return: The result of the operation call
    """
    client = hvac.Client(url=ctx.acct.get("address"), token=ctx.acct.get("token"))
    # Don't pass kwargs that have a "None" value to the function call
    kwargs = {k: v for k, v in op_kwargs.items() if v is not None}
    hub.log.debug(f"Getting raw results for {'.'.join(service_path)}.{operation}")
    op = getattr(client, service_path[0])
    for step in service_path[1:]:
        op = getattr(op, step)
    op = getattr(op, operation)
    return await hub.pop.loop.wrap(op, *op_args, **kwargs)
