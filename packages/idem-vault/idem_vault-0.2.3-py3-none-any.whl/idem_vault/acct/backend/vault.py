import re
from typing import Any
from typing import Dict

from dict_tools.data import NamespaceDict

VERSION_PATTERN = re.compile(r"^\w+(\d)(\.\d+)?$")


async def unlock(
    hub, *, address: str, token: str, path: str, version: str = "v2", **kwargs
) -> Dict[str, Dict[str, Any]]:
    """
    Use vault as a backend for storing acct profiles for other clouds.

    Include "acct-backends" in your acct_file and add the vault provider.
    You can have as many profiles as you need for the vault provider.

    .. code-block:: yaml

        acct-backends:
          vault:
            my_profile:
              address: http://127.0.0.1:8200
              token: Sb6lasdfsdf3ysfMNsdfd11
              path: my_path
              version: v1|v2

    The generic format for a secret containing acct profiles is:

    .. code-block:: python

        secret = {
            "provider_name": {
                "profile_name": {
                    "kwarg_1": "value_1",
                }
            },
        }

    A more specific example using aws and azure:

    .. code-block:: python

        secret = {
            "azure": {
                "default": {
                    "client_id": "12345678-1234-1234-1234-aaabc1234aaa",
                    "secret": "76543210-4321-4321-4321-bbbb3333aaaa",
                    "subscription_id": "ZzxxxXXXX11xx-aaaaabbbb-k3xxxxxx",
                    "tenant": "bbbbbca-3333-4444-aaaa-cddddddd6666",
                }
            },
            "aws": {
                "default": {
                    "aws_access_key_id": "xxxxxxxxxxxxxxxxx",
                    "aws_secret_access_key": "xxxxxxxxxxxxxxxxx",
                    "region_name": "us-west-1",
                }
            },
        }
    """
    ctx = NamespaceDict(acct=dict(address=address, token=token, version=version))
    result = {}

    for key in kwargs:
        hub.log.debug(f"Unknown kwarg passed to acct/backend/vault: {key}")

    version_match = VERSION_PATTERN.search(version)
    if version_match.group(1) == "1":
        secret_ret = await hub.exec.hvac.client.secrets.kv.v1.read_secret(
            ctx=ctx, path=path
        )
        secrets = secret_ret.ret.data
    elif version_match.group(1) == "2":
        secret_ret = await hub.exec.hvac.client.secrets.kv.v2.read_secret_version(
            ctx=ctx, path=path
        )
        secrets = secret_ret.ret.data.data
    else:
        raise ValueError(f"Unknown kv version: {version}")

    # If this fails, the profiles were improperly configured
    for provider_name, provider in secrets.items():
        if provider_name not in result:
            result[provider_name] = {}
        for profile_name, profile in provider.items():
            if profile_name not in result[provider_name]:
                result[provider_name][profile_name] = {}
            result[provider_name][profile_name] = profile

    return result
