import libhoney
import os
from dulwich.repo import Repo
from dulwich.porcelain import active_branch

from _assembly.sdk.pytest_plugin.fixtures.nodes_networks import load_network_config
from _assembly.sdk import get_network_config


# The dataset in Honeycomb where we persist metadata about test / benchmark run times etc.
HONEYCOMB_TESTDATA_DATASET = "Tests"


def metadata_fields(pytest_config):
    # Tag git metadata for this test
    git_info = {}

    try:
        repo = Repo.discover(".")
        commit_sha = repo.head().decode("utf-8")
        branch_name = active_branch(repo).decode("utf-8")
        git_info = {"branch": branch_name, "commit": commit_sha}
    except Exception:
        pass

    extra_fields = {
        "env": "local",
    }

    # Tag network tests
    network_name = pytest_config.getoption("--network-name")
    net_conf = pytest_config.getoption("--network-config")
    connection_file = pytest_config.getoption("--connection-file")

    if network_name is not None:
        network_config = get_network_config(network_name)
    elif connection_file is not None:
        network_config = connection_file
    elif net_conf is not None:
        network_config = net_conf
    else:
        network_config = get_network_config("default")

    nodes = load_network_config(network_config)
    num_nodes = len(nodes.sessions.keys())
    extra_fields["num_nodes"] = num_nodes
    if num_nodes > 0:
        extra_fields["nodeFqdn"] = list(nodes.sessions.keys())[0]
    extra_fields["env"] = "remote"

    fields = {
        "circleWorkflow": os.getenv("CIRCLE_WORKFLOW_ID", "NONE"),
        **git_info,
        **extra_fields,
    }
    return fields


def report_pytest_to_honeycomb(report, pytest_config):
    metadata = metadata_fields(pytest_config)

    fields = {
        "benchmark": False,
        "outcome": report.outcome,
        "duration_ms": report.duration * 1000,
        "name": report.location[2],
        **metadata,
    }
    event = libhoney.new_event()
    event.add(fields)
    event.send()


def report_benchmark_to_honeycomb(benchmark, pytest_config):
    metadata = metadata_fields(pytest_config)
    fn = benchmark.fullname
    class_name = fn.split(".py::")[1].split("::")[0]
    function_name = fn.split("::")[-1].split("[")[0]
    params = f"[{fn.split('[')[-1]}"
    data = benchmark.stats.data
    outcome = "failed" if benchmark.has_error else "passed"
    extra_info = benchmark.get("extra_info", {})

    for duration in data:
        fields = {
            "benchmark": True,
            "name": f"{class_name}.{function_name}{params}",
            "class_name": class_name,
            "function_name": function_name,
            "group": benchmark.group,
            "duration_ms": duration * 1000,
            "outcome": outcome,
            **metadata,
            **extra_info,
        }
        event = libhoney.new_event()
        event.add(fields)
        event.send()
