import os
import shutil
from junitparser import JUnitXml, Failure, Error, TestSuite, TestCase


def move_junit_and_validate(internal_junit_path, test_output_dir):
    """
    when we have the sdk launch itself inside a docker container, the junit output produced internally
    needs to be moved into a spot that can match the junit output location of the parent sdk invocation
    :param internal_junit_path: where the junit file lives internal to the sdk docker container
    :param test_output_dir: where test outputs are put from the wrapper sdk invocation
    """
    internal_junit_output_dir = f"{test_output_dir}/test-results/internal"
    os.makedirs(internal_junit_output_dir, exist_ok=True)
    shutil.copy(internal_junit_path, internal_junit_output_dir)
    check_for_errors(
        f"{internal_junit_output_dir}/{os.path.basename(internal_junit_path)}"
    )


def check_for_errors(junit_path):
    """
    when working with the wrapped sdk, one risk is that the internal process returns a successful exit
    code but the tests it ran actually failed. as a sanity check around that we read through the internal
    junit an check if any have failed.
    :param junit_path: path to a junit file on the host filesystem to check for errors
    """

    errors = []

    def traverse(elem):
        if isinstance(elem, TestSuite):
            for child in elem:
                traverse(child)
        elif isinstance(elem, TestCase):
            if isinstance(elem, Failure) or isinstance(elem, Error):
                errors.append(elem)

    traverse(JUnitXml.fromfile(junit_path))

    if len(errors) > 0:
        raise Exception(
            f"found {len(errors)} failures in checked junit file {junit_path}"
        )
