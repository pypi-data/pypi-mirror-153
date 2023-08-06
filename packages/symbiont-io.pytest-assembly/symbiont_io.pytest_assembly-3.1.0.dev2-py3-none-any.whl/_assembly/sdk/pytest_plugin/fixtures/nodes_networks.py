##########################
### nodes and networks ###
##########################

# a set of fixtures for managing and interacting with nodes, networks and associated low level kubernetes
# access.
#
### architectural themes
#
# * it is a conscious decision that each fixture either explicitly consumes output from another fixture,
#   or reads input directly from the pytest `request` fixture. as we already do a lot of input management
#   this way it is simplest to consistently use it for all our input management.
#
# * these fixtures are designed assuming a user can access the system at multiple levels, in some cases
#   they will want a fully built network and not think about anything, but in others they will want to
#   start with nothing more than a kubernetes context
#
# * abstraction by subclassing and not composition is used to enrich a set of nodes with kubernetes
#   functionality as it really truly is just nodes but with more functionality. using composition requires
#   a bunch of manual dispatch between the composed pieces that is undesirable
#
# * if users directly build their own network, they will want to build the various instances directly, so
#   the classes themselves must have high quality interfaces

import json
import os
import time


from assembly_client.api import node_api_client
from assembly_client.api.network_client import NetworkClient
from assembly_client.api.node_client import NodeSession
from _assembly.sdk.util.path_util import prep_path, prepare_cert
from _assembly.sdk import get_network_config

from assembly_client.api.job_management import Job, ContractErrorInJob
from assembly_client.api.types.error_types import ContractError


###############################
### user api and data model ###
###############################


class Nodes:
    """
    this is the raw set of nodes, and supports operations that one performs on nodes directly
    """

    def __init__(self, sessions, neo_key, neo_crt):
        # a simple dictionary of string node name to `NodeSession` from our http client
        self.sessions = sessions
        self.neo_key = neo_key
        self.neo_crt = neo_crt


#######################################
### fixture builder implementations ###
#######################################

### automatic postgres management

### network


class SyncNetworkClient(NetworkClient):
    def async_call(self, key_alias, contract_ref, function, kwargs):
        """
        calls the specified contract function on a node
        :param key_alias: key_alias to invoke as
        :param contract_ref: contract to call
        :param function: function to invoke
        :param kwargs: dictionary of arguments to the contract, will be json serialized
        :return: the result of the call as a value or job object
        """
        session = self.node_sessions[self.alias_locations[key_alias]]

        # if this clientside does not post, it'll be the value read, otherwise a job
        result = node_api_client.call(
            session,
            key_alias,
            contract_ref,
            function,
            kwargs,
            query_tx_index=self.query_tx_index,
        )
        self.query_tx_index = None

        if isinstance(result, Job):
            try:
                completed_job = result.start_waiting(timeout=self.timeout)
            except ContractErrorInJob as e:
                raise ContractError(e.msg, e.data)
            completed_job.network_client = self
            completed_job.sync_with(timeout=self.timeout)
            return completed_job.result["result"]
        return result


def network_fixture(nodes, sdk_args):
    network_client = SyncNetworkClient(
        nodes.sessions,
        sdk_args.contract_path,
        sdk_args.language_version,
        neo_key=nodes.neo_key,
        neo_crt=nodes.neo_crt,
        skip_consistency_check=sdk_args.skip_consistency_check,
        timeout=sdk_args.timeout,
    )
    network_client.wait_for_ready()
    return network_client


def nodes_fixture(sdk_args, tracer):
    """
    :return: `Nodes` instance for the specified network configuration
    """
    if sdk_args.network_name is not None:
        network_config = get_network_config(sdk_args.network_name)
    elif sdk_args.connection_file is not None:
        network_config = sdk_args.connection_file
    elif sdk_args.network_config is not None:
        network_config = sdk_args.network_config
    else:
        network_config = get_network_config("default")

    return load_network_config(network_config, tracer)


def load_network_config(config_path, tracer=None):
    """
    :param config_path: path to network configuration file on disk
    :return: an instance of `Nodes`
    """
    with open(prep_path(config_path)) as f:
        config = json.load(f)

    return create_nodes_from_network_config(config, tracer)


def create_nodes_from_network_config(config, tracer=None):
    """
    :param config: network configuration
    :return: an instance of `Nodes`
    """
    ### legacy support: if we don't have a top level `nodes` or `neo_config` key assume an old config. we can still
    ###                 load it, but will not be able to perform neo operations

    nodes = {}
    node_configs = config.get("nodes") or config
    for node_name, node_config in node_configs.items():

        admin_cert_name = node_config.get("admin_cert")
        admin_cert_key_name = node_config.get("admin_cert_key")
        client_cert_name = node_config.get("client_cert")
        client_cert_key_name = node_config.get("client_cert_key")

        nodes[node_name] = NodeSession(
            node_fqdn=node_name,
            hostname=node_config["hostname"],
            admin_certs=(
                prepare_cert(admin_cert_name, "admin", "crt", node_name),
                prepare_cert(admin_cert_key_name, "admin", "key", node_name),
            )
            if (admin_cert_name and admin_cert_key_name)
            else None,
            client_certs=(
                prepare_cert(client_cert_name, "client", "crt", node_name),
                prepare_cert(client_cert_key_name, "client", "key", node_name),
            )
            if (client_cert_name and client_cert_key_name)
            else None,
            tracer=tracer,
        )

    neo_key = None
    neo_crt = None
    if "neo_config" in config:
        neo_key = config["neo_config"]["private"].encode("utf-8")
        neo_crt = config["neo_config"]["public"].encode("utf-8")

    return Nodes(nodes, neo_key, neo_crt)
