import os
import subprocess
import json

DEFAULT_LANGUAGE_VERSION = 8


def get_network_config(network_name):
    ASSEMBLY_DEV_PATH = os.path.join(
        os.environ["SYMENV_DIR"], "versions/current/bin/assembly-dev"
    )

    assembly_dev_result, stderr = subprocess.Popen(
        [ASSEMBLY_DEV_PATH, "dev-network", "info", network_name],
        stdout=subprocess.PIPE,
    ).communicate()

    try:
        json_result = json.loads(assembly_dev_result)
        return json_result["network_config"]
    except:
        return os.path.join(
            os.environ["SYMENV_DIR"],
            f"assembly-dev/dev-network/{network_name}/network-config.json",
        )
