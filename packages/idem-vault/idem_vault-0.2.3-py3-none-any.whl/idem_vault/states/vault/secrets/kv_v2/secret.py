from typing import Dict

import dict_tools.data


async def present(
    hub,
    ctx,
    name: str,
    path: str,
    data: Dict,
    disable_read: bool = False,
) -> Dict:
    """
    Creates or update a secret stored with Vault KV_v2 secret engine.

    Args:
        name(string): An Idem name of the resource.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.
        data(string, optional): Data to be written in the format of a JSON object.
        disable_read(bool, optional): Set this field to True if the vault authentication does not have read access.
            However, if the value is True, this Idem state operation is not idempotent, and Idem state comment output
             will always assume it is a "create" operation. Defaults to False.

    Request Syntax:
        [vault-secret-name]:
          vault.secrets.kv_v2.secret.present:
          - path: 'string'
          - data: 'string'
          - disable_read: 'boolean'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-secret:
              vault.secrets.kv_v2.secret.present:
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
    # data is converted to SafeNamespaceDict to avoid it being converted to string and printed to console.
    data = dict_tools.data.SafeNamespaceDict(data)
    if not disable_read:
        read_ret = await hub.exec.hvac.client.secrets.kv.v2.read_secret_version(
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
                "data": dict_tools.data.SafeNamespaceDict(
                    read_ret["ret"]["data"]["data"]
                ),
            }
    else:
        hub.log.debug(f"vault.secrets.kv_v2.secret '{name}' read has been disabled.")
        result["comment"] = (
            f"vault.secrets.kv_v2.secret '{name}' read has been disabled.",
        )
    if (result["old_state"] is not None) and result["old_state"]["data"] == data:
        result["comment"] = result["comment"] + (
            f"vault.secrets.kv_v2.secret '{name}' has no property need to be updated.",
        )
        return result
    elif result["old_state"] is None:
        if ctx.get("test", False):
            result["comment"] = (f"Would create vault.secrets.kv_v2.secret '{name}'.",)
            result["new_state"] = {"name": name, "path": path, "data": data}
            return result
    else:
        if ctx.get("test", False):
            result["comment"] = (f"Would update vault.secrets.kv_v2.secret '{name}'.",)
            result["new_state"] = {"name": name, "path": path, "data": data}
            return result

    write_ret = await hub.exec.hvac.client.secrets.kv.v2.create_or_update_secret(
        ctx=ctx, path=path, secret=data
    )
    if not write_ret["result"]:
        result["result"] = False
        result["comment"] = write_ret["comment"]
        return result
    result["new_state"] = {"name": name, "path": path, "data": data}
    if result["old_state"] is None:
        result["comment"] = (f"Created vault.secrets.kv_v2.secret '{name}'.",)
    else:
        result["comment"] = (f"Updated vault.secrets.kv_v2.secret '{name}'.",)
    return result


async def absent(
    hub, ctx, name: str, path: str, delete_all_versions: bool = False
) -> Dict:
    """
    Delete a secret stored with Vault KV_v2 secret engine.

    Args:
        name(string): An Idem name of the resource.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.
        delete_all_versions(bool, optional): Set this field to True if the vault authentication does not have read access.
            However, if the value is True, this Idem state operation is not idempotent. Defaults to False.

    Request Syntax:
        [vault-secret-name]:
          vault.secrets.kv_v2.secret.absent:
          - path: 'string'
          - delete_all_versions: 'boolean'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-secret:
              vault.secrets.kv_v2.secret.absent:
                - path: secret/test
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": (),
    }
    read_ret = await hub.exec.hvac.client.secrets.kv.v2.read_secret_version(
        ctx=ctx, path=path
    )
    if not read_ret["result"]:
        if "InvalidPath" in str(read_ret["comment"]):
            result["comment"] = (
                f"vault.secrets.kv_v2.secret '{name}' is already absent.",
            )
        else:
            result["result"] = False
            result["comment"] = read_ret["comment"]
        return result

    # "data" is not populated to reduce data exposure.
    result["old_state"] = {"name": name, "path": path}
    delete_version = [read_ret["ret"]["data"]["metadata"]["version"]]
    if delete_all_versions:
        version_ret = await hub.exec.hvac.client.secrets.kv.v2.read_secret_metadata(
            ctx=ctx, path=path
        )
        if not version_ret["result"]:
            result["result"] = False
            result["comment"] = version_ret["comment"]
            return result
        delete_version = list(version_ret["ret"]["data"]["versions"].keys())
    if ctx.get("test", False):
        if delete_all_versions:
            result["comment"] = (
                f"Would delete vault.secrets.kv_v2.secret '{name}' all versions.",
            )
        else:
            result["comment"] = (f"Would delete vault.secrets.kv_v2.secret '{name}'.",)
        return result
    delete_ret = await hub.exec.hvac.client.secrets.kv.v2.destroy_secret_versions(
        ctx=ctx, path=path, versions=delete_version
    )
    if not delete_ret["result"]:
        result["result"] = False
        result["comment"] = read_ret["comment"]
    elif delete_all_versions:
        result["comment"] = (
            f"Deleted vault.secrets.kv_v2.secret '{name}' all versions.",
        )
    else:
        result["comment"] = (f"Deleted vault.secrets.kv_v2.secret '{name}'.",)
    return result


async def search(hub, ctx, name, path: str, version: int = None) -> Dict:
    """
    KV_v2 secret data-source.

    Args:
        name(string): The name of the Idem state.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.
        version(int, optional): The version of the secret to read. If not specified, the latest version will be used.

    Request Syntax:
        [Idem-state-name]:
          vault.secrets.kv_v2.secret.search:
          - path: 'string'
          - version: 'int'

        Examples:

            my-secret:
              vault.secrets.kv_v2.secret.search:
                - path: secret/test
                - version: 1
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": (),
    }
    read_ret = await hub.exec.hvac.client.secrets.kv.v2.read_secret_version(
        ctx=ctx, path=path, version=version
    )
    if not read_ret["result"]:
        result["result"] = False
        result["comment"] = read_ret["comment"]
        return result
    result["old_state"] = {
        "name": name,
        "path": path,
        "data": dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"]["data"]),
    }
    result["new_state"] = {
        "name": name,
        "path": path,
        "data": dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"]["data"]),
    }
    return result
