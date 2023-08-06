import os


def test_pytest_plugin(testdir):

    # create a temporary conftest.py file
    testdir.makeconftest(
        """
        import pytest
        from _assembly.sdk.pytest_plugin.plugin import *
        from assembly_client.api.contracts import ContractRef

        @pytest.fixture
        def reset(network):
            network.reset(txe_protocol=13, sympl_version=10)

        @pytest.fixture
        def async_reset(async_network):
            async_network.reset(txe_protocol=13, sympl_version=10)

        @pytest.fixture
        def contracts(network, reset):
            network.publish(
                [ContractRef("data", "1.0.0", 10),
                ContractRef("hello", "1.0.0", 10),
                ContractRef("hello", "1.0.1", 10)],
            )

        @pytest.fixture
        def async_contracts(async_network, async_reset):
            os.environ["CONTRACT_PATH"] = "contracts"
            async_network.publish(
                [ContractRef("data", "1.0.0", 10)]
            )

        @pytest.fixture
        def key_alias(network, reset, store):
            store["default_ka"] = network.register_key_alias()
            return network[store["default_ka"]]

        @pytest.fixture
        def async_key_alias(async_network, async_reset, store):
            store["default_ka"] = async_network.register_key_alias()
            return async_network[store["default_ka"]]
        """
    )

    testdir.makepyfile(
        """
        import pytest
        import re
        from assembly_client.api.types.error_types import ContractError
        from _assembly.sdk.util.timeout import network_timeout_as

        def test_network(network, reset):
            assert network is not None

        def test_async_network(async_contracts, async_network, async_reset, async_key_alias):
            assert async_network is not None
            assert len(async_network.list_key_aliases()) == 1
            job = async_key_alias.data["10-1.0.0"].run_executable().start_waiting().sync_with()
            assert "foo" == job.result["result"]

        def test_executable_return_value_with_timeout(contracts, network, key_alias):
            with network_timeout_as(key_alias, 0):
                with pytest.raises(Exception, match="but was not found after waiting for 0s"):
                    key_alias.data["10-1.0.0"].run_executable()

        def test_network_timeout_as_type_check(contracts, network, key_alias):
            with pytest.raises(Exception, match=re.escape("Only type <class 'assembly_client.api.network_client.KeyAliasClient'> is supported. Client can be obtained calling network[<key_alias>].")):
                with network_timeout_as("foo", 0):
                    key_alias.data["10-1.0.0"].run_executable()

        def test_list_contracts(network, reset):
            assert [] == network.list_contracts()

        def test_list_ka(network, reset):
            assert [] == network.list_key_aliases()

        def test_create_ka(network, reset):
            network.register_key_alias()
            assert len(network.list_key_aliases()) == 1

        def test_publish(contracts, network):
            assert 3 == len(network.list_contracts())

        def test_executable_return_value(contracts, network, key_alias):
            assert len(network.list_key_aliases()) == 1
            assert "foo" == key_alias.data["10-1.0.0"].run_executable()

        def test_clientside_return_value(contracts, network, key_alias):
            assert len(network.list_key_aliases()) == 1
            assert "bar" == key_alias.data["10-1.0.0"].run_clientside()

        def test_clientside_error(contracts, network, key_alias):
            with pytest.raises(ContractError, match="This is a clientside error"):
                key_alias.data["10-1.0.0"].run_clientside_error()

        def test_executable_error(contracts, network, key_alias):
            with pytest.raises(ContractError, match="This is an executable error"):
                key_alias.data["10-1.0.0"].run_executable_error()

        def test_timeout_is_set(network, key_alias):
            assert network.timeout == 181
            assert key_alias.network_client.timeout == 181
        """
    )

    result = testdir.runpytest(
        f"--contract-path={os.path.dirname(os.path.realpath(__file__)) + '/contracts/data'}",
        f"--contract-path={os.path.dirname(os.path.realpath(__file__)) + '/contracts/hello'}",
        "--timeout=181",
    )
    result.assert_outcomes(passed=13)
