import pytest

from _assembly.sdk.pytest_plugin.fixtures.pytest_args import PytestArgs


def run_marker_setup(item):

    # directly build an `sdk_args` as we can't pull a fixture here
    sdk_args = PytestArgs(item)

    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.skip("previous test failed (%s)" % previousfailed.name)

    if "fails_remote" in item.keywords:
        if sdk_args.network_config:
            pytest.skip("flagged as failing remote: {}".format(item.name))

    if "requires_network" in item.keywords:
        if sdk_args.skip_requires_network or not (
            sdk_args.network_config
            or sdk_args.build_k8s_network
            or sdk_args.network_name
        ):
            pytest.skip(
                "requires multi node network but currently running in local mode"
            )

    propmarker = item.get_closest_marker("proptest")
    if propmarker:
        if not sdk_args.proptests:
            pytest.skip("test requires --proptests")

    benchmark_marker = item.get_closest_marker("benchmark")
    if benchmark_marker:
        if not sdk_args.benchmarks:
            pytest.skip("test requires --benchmarks")
        else:
            item.config.pluginmanager.getplugin("pytest-benchmark")
            if sdk_args.baseline:
                parametrize_marker = item.get_closest_marker("parametrize")
                if parametrize_marker and parametrize_marker.args[1][0]:
                    baseline_parameters = parametrize_marker.args[1][0]
                else:
                    baseline_parameters = ""

                # test name and parameterization (i.e. [5-50000-5]) lookup in 'test_creating_chunks[5-50000-5]'
                baseline_param_string = (
                    str(baseline_parameters)
                    .replace(", ", "-")
                    .replace("(", "[")
                    .replace(")", "]")
                )

                # Handles single parameters with non-tuple values (i.e. [12])
                if not isinstance(baseline_parameters, tuple):
                    baseline_param_string = f"[{baseline_param_string}]"

                if baseline_parameters != "" and baseline_param_string not in item.name:
                    pytest.skip("Skip parameterization: {}".format(item.name))
