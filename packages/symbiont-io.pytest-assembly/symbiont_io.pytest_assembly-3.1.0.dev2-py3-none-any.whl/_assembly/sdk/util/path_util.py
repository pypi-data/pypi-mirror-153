import os
import glob


class PathDoesNotExistError(Exception):
    pass


def prep_path(path):
    """prepare the path for use"""

    expanded = os.path.expandvars(os.path.expanduser(path))

    def check_exists(path):
        if not os.path.isfile(path) and not os.path.isdir(path):
            raise PathDoesNotExistError(
                "Error: file or directory does not exist - {}".format(path)
            )

    if os.path.isabs(expanded):
        check_exists(expanded)
        return expanded
    else:
        abs = os.path.join(os.getcwd(), expanded)
        check_exists(abs)
        return abs


def files_from(path):
    """given a path, return all python files present, excluding __init__.py"""
    if path.endswith(".py") and not path.startswith("__init__"):
        return [prep_path(path)]
    else:
        return sum([files_from(r) for r in glob.glob(path + "**/*.py")], [])


def prepare_cert(cert_string, cert_prefix, cert_type, hostname):
    """
    Write a certificate to disk for use with `requests`, given the certificate in PEM format
    """
    if cert_string is None:
        return None
    cert_path = "/tmp/{}-{}.{}".format(cert_prefix, hostname, cert_type)
    with os.fdopen(os.open(cert_path, os.O_WRONLY | os.O_CREAT, mode=0o600), "w") as f:
        f.write("{}\n".format(cert_string))
    cert = prep_path(cert_path)
    return cert
