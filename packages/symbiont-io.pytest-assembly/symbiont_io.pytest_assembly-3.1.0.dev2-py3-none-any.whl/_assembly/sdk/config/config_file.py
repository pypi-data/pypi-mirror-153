######################################
### configuration file for the sdk ###
######################################

# this module provides a configuration file for the sdk, which can be used to override and set various
# values normally provided through cli arguments. some are global defaults, others are specified by defining
# an `environment` which can be used as a shortcut to name a package of arguments
#
# architectural concerns:
#
# * we've chosen an unstructured format for this configuration information for ease of use. as we don't have
#   any complex structure in configs, simply a list of allowed keys in dictionaries captures everything we
#   need to capture to perform validation


import json

from _assembly.sdk.util.path_util import prep_path, PathDoesNotExistError
from _assembly.sdk.config.options import CONFIG_OPTIONS

# this drops the first two characters (--) and then converts any snake-case to underscore_case as that is how
# we reference config values in json
VALID_CONFIG_KEYS = [row[0][2:].replace("-", "_") for row in CONFIG_OPTIONS]


class InvalidConfigurationException(Exception):
    pass


def validate_config(config_dict):
    """
    using our list of defined keys that are actually checked, ensure no additional keys are present in the config
    which will be ignored
    :param config_dict: configuration loaded as json
    :return: `None` is valid, raises `Exception` if invalid
    """

    if "defaults" not in config_dict:
        raise InvalidConfigurationException(
            "invalid configuration file: missing `defaults`"
        )
    if "environments" not in config_dict:
        raise InvalidConfigurationException(
            "invalid configuration file: missing `environments`"
        )
    if "defaults" in config_dict["environments"]:
        raise InvalidConfigurationException(
            "invalid configuration file: illegal environment name `defaults`"
        )


def read_config_file(config_path=None):
    """
    read a configuration file at ~/.config/symbiont/python-sdk.json
    :param path: optional, if present override default file location
    :return: `SdkConfig` instance loaded with found values if path is found
    """

    config_path_or_default = (
        config_path or "$HOME/.config/symbiont/python-sdk-config.json"
    )

    try:
        with open(prep_path(config_path_or_default)) as f:
            config_dict = json.load(f)
    except PathDoesNotExistError as e:
        # only allow not finding a config if none was explicitly passed
        if config_path:
            raise e
        else:
            return None

    validate_config(config_dict)

    return config_dict


def get_config_value(config, key, env=None):
    if not config:
        return None
    if env and env not in config["environments"]:
        # if we are looking for a non-existent environment this is a failure
        raise InvalidConfigurationException(f"environment not found in config: {env}")
    elif env and key in config["environments"][env]:
        # if the environment is there and has the key use that value
        value = config["environments"][env][key]
    else:
        # if no environment or it did not have the key we try defaults. if not there will return `None`
        value = config["defaults"].get(key)

    return value
