from hypothesis import settings, Verbosity, HealthCheck
from hypothesis.stateful import run_state_machine_as_test


def build_hypothesis_settings(sdk_args):
    """run a much longer version of property tests, it will be a dedicated nightly build"""
    if (sdk_args.baseline is not None) and sdk_args.baseline:
        return settings(
            max_examples=5,
            deadline=None,
            suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow],
        )
    else:
        return settings(
            max_examples=500,
            verbosity=Verbosity.debug,
            deadline=None,
            suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow],
        )


class ModelTestWithNetworkRunner:
    """
    deals with wiring a `network` instance for the caller, just providing a simple
    `run` method for invoking model tests. can thread both hypothesis settings and
    extra model class arguments through.
    """

    def __init__(self, network):
        self.network = network

    def run(self, cls, settings=None, **extra_kwargs):
        def factory(*args, **kwargs):
            return cls(*args, **kwargs, network=self.network, **extra_kwargs)

        factory.__name__ = cls.__name__
        run_state_machine_as_test(factory, settings=settings)
