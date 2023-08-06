from contextlib import contextmanager
from assembly_client.api.network_client import KeyAliasClient


@contextmanager
def network_timeout_as(ka_client, timeout):
    """Manually set the network timeout for a KeyAliasClient

    :param ka_client KeyAliasClient: Client to adjust the timeout of.
    :param timeout int: Timeout in seconds.
    """
    if not isinstance(ka_client, KeyAliasClient):
        raise TypeError(
            f"Only type {KeyAliasClient} is supported. Client can be obtained calling network[<key_alias>]."
        )

    old_timeout = ka_client.network_client.timeout
    ka_client.network_client.timeout = timeout
    yield
    ka_client.network_client.timeout = old_timeout
