import json
from json.decoder import JSONDecodeError
from typing import Dict

import dict_tools.data


async def present(
    hub,
    ctx,
    name: str,
    path: str,
    data: str or Dict,
    disable_read: bool = False,
) -> Dict:
    """
    Creates or update a secret stored with Vault KV_v1 secret engine.

    Args:
        name(string): An Idem name of the resource.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.
        data(string or dict, optional): Data to be written in the format of a JSON string or a JSON object that can be stringfied.
        disable_read(bool, optional): Set this field to True if the vault authentication does not have read access.
            However, if the value is True, this Idem state operation is not idempotent, and Idem state comment output
             will always assume it is a "create" operation. Defaults to False.

    Request Syntax:
        [vault-secret-name]:
          vault.secrets.kv_v1.secret.present:
          - path: 'string'
          - data: 'string or dict'
          - disable_read: 'boolean'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-secret:
              vault.secrets.kv_v1.secret.present:
                - path: secret/test
                - data: '{"my-birthday": "2012-10-17"}'
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": (),
    }
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except JSONDecodeError as e:
            result[
                "comment"
            ] = f"Fail to load data {data} as json object: {e.__class__.__name__}: {e}"
            result["result"] = False
            return result
    # data is converted to SafeNamespaceDict to avoid it being converted to string and printed to console.
    data = dict_tools.data.SafeNamespaceDict(data)
    if not disable_read:
        read_ret = await hub.exec.hvac.client.secrets.kv.v1.read_secret(
            ctx=ctx, path=path
        )
        if not read_ret["result"]:
            if "InvalidPath" not in str(read_ret["comment"]):
                result["result"] = False
                result["comment"] = read_ret["comment"]
                return result
        else:
            result["old_state"] = {
                "name": name,
                "path": path,
                "data": dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"]),
            }
    else:
        hub.log.debug(f"vault.secrets.kv_v1.secret '{name}' read has been disabled.")
        result["comment"] = (
            f"vault.secrets.kv_v1.secret '{name}' read has been disabled.",
        )
    if (result["old_state"] is not None) and result["old_state"]["data"] == data:
        result["comment"] = result["comment"] + (
            f"vault.secrets.kv_v1.secret '{name}' has no property need to be updated.",
        )
        return result
    elif result["old_state"] is None:
        if ctx.get("test", False):
            result["comment"] = (f"Would create vault.secrets.kv_v1.secret '{name}'.",)
            result["new_state"] = {"name": name, "path": path, "data": data}
            return result
    else:
        if ctx.get("test", False):
            result["comment"] = (f"Would update vault.secrets.kv_v1.secret '{name}'.",)
            result["new_state"] = {"name": name, "path": path, "data": data}
            return result

    write_ret = await hub.exec.hvac.client.secrets.kv.v1.create_or_update_secret(
        ctx=ctx, path=path, secret=data
    )
    if not write_ret["result"]:
        result["result"] = False
        result["comment"] = write_ret["comment"]
        return result
    result["new_state"] = {"name": name, "path": path, "data": data}
    if result["old_state"] is None:
        result["comment"] = (f"Created vault.secrets.kv_v1.secret '{name}'.",)
    else:
        result["comment"] = (f"Updated vault.secrets.kv_v1.secret '{name}'.",)
    return result


async def absent(
    hub,
    ctx,
    name: str,
    path: str,
) -> Dict:
    """
    Delete a secret stored with Vault KV_v1 secret engine.

    Args:
        name(string): An Idem name of the resource.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.

    Request Syntax:
        [vault-secret-name]:
          vault.secrets.kv_v1.secret.absent:
          - path: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-secret:
              vault.secrets.kv_v1.secret.absent:
                - path: secret/test
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": (),
    }
    read_ret = await hub.exec.hvac.client.secrets.kv.v1.read_secret(ctx=ctx, path=path)

    if not read_ret["result"]:
        if "InvalidPath" in str(read_ret["comment"]):
            result["comment"] = (
                f"vault.secrets.kv_v1.secret '{name}' is already absent.",
            )
        else:
            result["result"] = False
            result["comment"] = read_ret["comment"]
        return result

    # "data" is not populated to reduce data exposure.
    result["old_state"] = {"name": name, "path": path}
    if ctx.get("test", False):
        result["comment"] = (f"Would delete vault.secrets.kv_v1.secret '{name}'.",)
        return result
    delete_ret = await hub.exec.hvac.client.secrets.kv.v1.delete_secret(
        ctx=ctx, path=path
    )
    if not delete_ret["result"]:
        result["result"] = False
        result["comment"] = read_ret["comment"]
    else:
        result["comment"] = (f"Deleted vault.secrets.kv_v1.secret '{name}'.",)
    return result


async def search(hub, ctx, name, path: str) -> Dict:
    """
    KV_v1 secret data-source.

    Args:
        name(string): The name of the Idem state.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.

    Request Syntax:
        [Idem-state-name]:
          vault.secrets.kv_v1.secret.search:
          - path: 'string'

        Examples:

            my-secret:
              vault.secrets.kv_v1.secret.search:
                - path: secret/test
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": (),
    }
    read_ret = await hub.exec.hvac.client.secrets.kv.v1.read_secret(ctx=ctx, path=path)

    if not read_ret["result"]:
        result["result"] = False
        result["comment"] = read_ret["comment"]
        return result
    result["old_state"] = {
        "name": name,
        "path": path,
        "data": dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"]),
    }
    result["new_state"] = {
        "name": name,
        "path": path,
        "data": dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"]),
    }
    return result
