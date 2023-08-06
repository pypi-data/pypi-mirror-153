import pytest


class TestPytestPlugin:
    @pytest.fixture
    def reset(self, network):
        network.reset()

    def test_network(self, network, reset):
        assert network is not None

    def test_list_contracts(self, network, reset):
        assert [] == network.list_contracts()

    def test_list_ka(self, network, reset):
        assert [] == network.list_key_aliases()

    def test_create_ka(self, network, reset):
        network.register_key_alias()
        assert len(network.list_key_aliases()) == 1
