from _assembly.sdk.config.options import CONFIG_OPTIONS

# these arguments come from the sdk configuration module, and are simply inserted here. this is not the formal
# source of truth as we also want to use that set to validate configuration files


def add_pytest_arguments(parser):
    try:
        for row in CONFIG_OPTIONS:
            extra_args = row[3] if len(row) == 4 else {}
            # for boolean values we massage a more consistent definition schema into the argparse expectations
            if row[1] == bool:
                parser.addoption(row[0], action="store_true", help=row[2], **extra_args)
            else:
                if "action" not in extra_args:
                    extra_args["action"] = "store"

                parser.addoption(row[0], type=row[1], help=row[2], **extra_args)
    except ValueError:
        # options already configured, skip
        pass
