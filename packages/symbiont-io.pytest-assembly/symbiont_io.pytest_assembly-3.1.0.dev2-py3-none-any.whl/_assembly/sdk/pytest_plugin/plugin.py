import pytest
import time
import urllib3
import beeline
import datetime
import os
import libhoney


from _assembly.sdk.pytest_plugin.arguments import add_pytest_arguments
from _assembly.sdk.pytest_plugin.markers import run_marker_setup

from _assembly.sdk.pytest_plugin.honeycomb_reporting import (
    report_benchmark_to_honeycomb,
    report_pytest_to_honeycomb,
)
from _assembly.sdk.pytest_plugin.honeycomb_reporting import HONEYCOMB_TESTDATA_DATASET
from _assembly.sdk.pytest_plugin.fixtures import property_testing
from _assembly.sdk.pytest_plugin.fixtures import nodes_networks
from _assembly.sdk.pytest_plugin.fixtures.pytest_args import PytestArgs

from _assembly.lib.util.crypto import new_nonce
from _assembly.lib.util.log import setup_sdk_logging
from assembly_client.api.network_client import NetworkClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# This is to solve the problem of not having access to pytest config from certain hooks.
# Interestingly I could not find many solutions to this problem online even though I spend hours searching.
# So the idea that worked is to save config globally (scoped inside this trivial class) in the pytest_configure
# to make it available for pytest_runtest_logreport hook that uses it to extract command line options.
# I realize that this solution is quite dirty (as it pollutes the global state) but unfortunately I could not find
# any other way to make this work.
# To fix this properly would require redesigning/rethinking things, which requires expertise with pytest that
# I do not yet possess.


####################
### pytest hooks ###
####################


class PytestUtil:
    config = None


def pytest_addoption(parser):
    return add_pytest_arguments(parser)


def pytest_runtest_setup(item):
    return run_marker_setup(item)


def pytest_runtest_logreport(report):
    if report.when == "call":
        for m in report.markers:
            if m.name == "benchmark" or (
                m.name == "usefixtures" and ("benchmark" in m.args)
            ):
                return
        report_pytest_to_honeycomb(report, PytestUtil.config)
        libhoney.flush()  # Ensure we send all data


def pytest_configure(config):
    PytestUtil.config = config

    # benchmark_save has to be set if we want to report data to honeycomb,
    # otherwise pytest_benchmark_generate_json below won't fire.
    # if the flag isn't passed, we set it to a dummy value here so we don't lose any data.
    if config.option.honeycomb_api_key and not config.option.benchmark_save:
        config.option.benchmark_save = "benchmark-results.json"
    config.addinivalue_line(
        "markers",
        "proptest: mark test as an expensive property test that only runs with --proptests",
    )
    config.addinivalue_line(
        "markers", "incremental: mark test as a depenent of a previous one"
    )


def pytest_benchmark_generate_json(
    config, benchmarks, include_data, machine_info, commit_info
):
    for benchmark in benchmarks:
        report_benchmark_to_honeycomb(benchmark, PytestUtil.config)
    libhoney.flush()  # Ensure we send all data


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    # an incremental marker for classes that makes a class stop on first failure,
    # taken from http://doc.pytest.org/en/latest/example/simple.html
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item

    # set data on the test items so that we can check in fixtures if tests passed or failed
    # https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures

    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(rep, "markers", list(item.iter_markers()))
    setattr(item, "rep_" + rep.when, rep)


#######################
### pytest fixtures ###
#######################

### testing basics


@pytest.fixture(scope="class")
def store():
    """a dictionary for passing data between tests in a class"""
    return {}


### network


@pytest.fixture(scope="class")
def async_network(nodes, sdk_args):
    """a network client that allows invoking contract functions, either locally or remote"""
    network = network_client = NetworkClient(
        nodes.sessions,
        sdk_args.contract_path,
        sdk_args.language_version,
        neo_key=nodes.neo_key,
        neo_crt=nodes.neo_crt,
        skip_consistency_check=sdk_args.skip_consistency_check,
        timeout=sdk_args.timeout,
    )
    network_client.wait_for_ready()
    yield network

    if "benchmark" not in sdk_args.request.fixturenames:
        network.consistency_check()


@pytest.fixture(scope="class")
def network(nodes, sdk_logger, sdk_args):
    """a network client that allows invoking contract functions, either locally or remote"""
    network = nodes_networks.network_fixture(nodes, sdk_args)
    yield network

    if "benchmark" not in sdk_args.request.fixturenames:
        network.consistency_check()


@pytest.fixture(scope="class")
def nodes(sdk_args, tracer):
    """direct access to the nodes for an associated network, safe for any remote network type"""
    return nodes_networks.nodes_fixture(sdk_args, tracer)


### hypothesis testing


@pytest.fixture
def hypothesis_settings(sdk_args):
    """check command line args and parameterize hypothesis appropriately"""
    return property_testing.build_hypothesis_settings(sdk_args)


@pytest.fixture(scope="class")
def model_tester(network):
    """wrap up hypothesis's model tester with a network fixture for convenience"""
    return property_testing.ModelTestWithNetworkRunner(network)


### run methods


@pytest.fixture(scope="session")
def sdk_args(request):
    """
    provide access to configuration data post argument parsing and config file merging
    """
    return PytestArgs(request)


### utils


@pytest.fixture(scope="session")
def sdk_logger(request, sdk_args):
    """
    initialize logging for the sdk
    """
    log_file = f"assembly-sdk-pytest-{datetime.datetime.today().isoformat()}.log"
    if sdk_args.output_dir:
        os.makedirs(sdk_args.output_dir, exist_ok=True)
        log_file = f"{sdk_args.output_dir}/{log_file}"
    setup_sdk_logging("assembly-sdk", sdk_args.sdk_log_level, log_file)


### tracing


class Tracer:
    def __init__(self, root_span, writekey, dataset, service_name):
        self.trace_id = root_span.trace_id
        self.root_span = root_span.id
        self.span = root_span.id
        self.writekey = writekey
        self.dataset = dataset
        self.service_name = service_name
        self.pid = os.getpid()

    @property
    def id(self):
        return self.root_span

    def set_span(self, span):
        self.span = span.id

    def get_nonce(self):
        return new_nonce()


@pytest.fixture(scope="session", autouse=True)
def tracer(sdk_args):
    tracer = None
    span = None
    if (
        sdk_args.honeycomb_api_key is not None
        and sdk_args.honeycomb_dataset is not None
        and sdk_args.tracing
    ):
        # This is for tracing local network operations, eg. when diagnosing local test performance
        # Supply --honeycomb-dataset, --honeycomb-api-key and --tracing to enable
        writekey = sdk_args.honeycomb_api_key
        dataset = sdk_args.honeycomb_dataset
        service_name = "local-network"
        honeycomb_host = sdk_args.honeycomb_host or "https://api.honeycomb.io"
        beeline.init(
            writekey=writekey,
            dataset=dataset,
            service_name=service_name,
            api_host=honeycomb_host,
        )
        span = beeline.start_trace(trace_id=new_nonce(), context={"name": "pytest"})
        tracer = Tracer(span, writekey, dataset, service_name)

    # We use the lower-level libhoney to send test duration + metadata to Honeycomb
    # Supply --honeycomb-api-key to enable
    if sdk_args.honeycomb_api_key is not None:
        libhoney.init(
            writekey=sdk_args.honeycomb_api_key,
            dataset=HONEYCOMB_TESTDATA_DATASET,
        )
    yield tracer
    if tracer is not None:
        beeline.finish_trace(span)
        beeline.close()
    libhoney.flush()


@pytest.fixture(scope="function", autouse=True)
def tracer_function(sdk_args, tracer, tracer_class, request):
    if tracer is not None:
        parent_id = tracer.id
        if tracer_class is not None:
            parent_id = tracer_class.id
        span = beeline.start_span(
            context={"name": request.node.name}, parent_id=parent_id
        )
        tracer.set_span(span)
        yield span
        beeline.finish_span(span)
    else:
        yield None


@pytest.fixture(scope="class", autouse=True)
def tracer_class(sdk_args, tracer, request):
    if tracer is not None:
        cls = request.cls
        if cls is not None:
            span = beeline.start_span(
                context={"name": request.cls.__name__}, parent_id=tracer.id
            )
            yield span
            beeline.finish_span(span)
        else:
            yield None
    else:
        yield None


### multiprocessing
def _is_local(sdk_args):
    return sdk_args.pool_debug or (
        sdk_args.network_config is None
        and sdk_args.network_name is None
        and sdk_args.build_k8s_network is None
    )


@pytest.fixture(scope="session")
def pool(sdk_args):
    nprocs = sdk_args.pool_nprocs
    with Pool(nprocs, _is_local(sdk_args)) as p:
        yield p


@pytest.fixture(scope="session")
def rpool(sdk_args):
    nprocs = sdk_args.pool_nprocs
    with ResizablePool(nprocs, _is_local(sdk_args)) as p:
        yield p


@pytest.fixture(scope="class")
def sleep(nodes):
    return (lambda s: None) if nodes is None else time.sleep


@pytest.fixture
def storage(network):
    storage_mock = StorageMock(network)
    yield storage_mock
    storage_mock.restore_original()
