from typing import Dict

import dict_tools.data

TREQ = {
    "unique": ["present", "absent"],
}


async def present(
    hub,
    ctx,
    name: str,
    path: str,
    key: str,
    value: str,
) -> Dict:
    """
    Creates or update a secret key stored with Vault KV_v1 secret engine.

    Args:
        name(string): An Idem name of the resource.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.
        key(string): Key of the secret
        value(string, optional): Value of the secret

    Request Syntax:
        [vault-secret-name]:
          vault.secrets.kv_v1.key.present:
          - path: 'string'
          - key: 'string'
          - value: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-secret:
              vault.secrets.kv_v1.key.present:
                - path: secret/test
                - key: my-birthday
                - value: 2012-10-17
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": (),
    }
    read_ret = await hub.exec.hvac.client.secrets.kv.v1.read_secret(ctx=ctx, path=path)
    data_to_update = {}
    if not read_ret["result"]:
        if "InvalidPath" not in str(read_ret["comment"]):
            result["result"] = False
            result["comment"] = read_ret["comment"]
            return result
    else:
        data_to_update = dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"])
        if data_to_update.get(key):
            result["old_state"] = {
                "name": name,
                "path": path,
                "key": key,
                "value": data_to_update.get(key),
            }

    action = "create" if data_to_update.get(key) is None else "update"
    if (
        result["old_state"] is not None
        and result["old_state"]["key"] == key
        and result["old_state"]["value"]
        and result["old_state"]["value"] == value
    ):
        result["comment"] = (
            f"vault.secrets.kv_v1.key '{name}' nothing to be updated.",
        )
        return result

    if ctx.get("test", False):
        result["new_state"] = {"name": name, "path": path, "key": key, "value": value}
        result["comment"] = (f"Would {action} vault.secrets.kv_v1.key '{key}'.",)
        return result

    data_to_update[key] = value
    write_ret = await hub.exec.hvac.client.secrets.kv.v1.create_or_update_secret(
        ctx=ctx, path=path, secret=data_to_update
    )
    if not write_ret["result"]:
        result["result"] = False
        result["comment"] = write_ret["comment"]
        return result
    result["new_state"] = {"name": name, "path": path, "key": key, "value": value}
    if result["old_state"] is None or "create" == action:
        result["comment"] = (f"Created vault.secrets.kv_v1.key '{key}'.",)
    else:
        result["comment"] = (f"Updated vault.secrets.kv_v1.key '{key}'.",)
    return result


async def absent(
    hub,
    ctx,
    name: str,
    path: str,
    key: str,
) -> Dict:
    """
    Delete a secret key stored with Vault KV_v1 secret engine.

    Args:
        name(string): An Idem name of the resource.
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.
        key(string): Secret key to the deleted

    Request Syntax:
        [vault-secret-name]:
          vault.secrets.kv_v1.key.absent:
          - path: 'string'
          - key: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-secret:
              vault.secrets.kv_v1.key.absent:
                - path: secret/test
                - key: my-birthday
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": (),
    }
    current_data = {}
    read_ret = await hub.exec.hvac.client.secrets.kv.v1.read_secret(ctx=ctx, path=path)

    if not read_ret["result"]:
        if "InvalidPath" in str(read_ret["comment"]):
            result["comment"] = (f"vault.secrets.kv_v1.key '{key}' is already absent.",)
        else:
            result["result"] = False
            result["comment"] = read_ret["comment"]
        return result

    current_data = dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"])
    if key not in current_data:
        result["comment"] = (f"vault.secrets.kv_v1.key '{key}' is already absent.",)
        return result

    # "data" is not populated to reduce data exposure.
    result["old_state"] = {"name": name, "path": path}

    if key not in current_data:
        result["comment"] = (f"vault.secrets.kv_v1.key '{key}' is already absent.",)
        return result

    if ctx.get("test", False):
        result["comment"] = (f"Would delete vault.secrets.kv_v1.key '{key}'.",)
        return result

    del current_data[key]
    if not current_data:
        # Delete path if all keys are removed. Path cannot exist with no keys
        ret = await hub.exec.hvac.client.secrets.kv.v1.delete_secret(ctx=ctx, path=path)
    else:
        ret = await hub.exec.hvac.client.secrets.kv.v1.create_or_update_secret(
            ctx=ctx, path=path, secret=current_data
        )

    if not ret["result"]:
        result["result"] = False
        result["comment"] = read_ret["comment"]
    else:
        result["comment"] = (f"Deleted vault.secrets.kv_v1.key '{key}'.",)
    return result
