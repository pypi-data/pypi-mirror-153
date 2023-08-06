class PytestArgs:
    def __init__(self, request):
        self.request = request

    def __getattr__(self, item):

        hyphenated = item.replace("_", "-")
        cli_formatted = f"--{hyphenated}"
        try:
            value = self.request.config.getoption(cli_formatted)
        except ValueError:
            value = None

        # if not found in either, return `None`
        return value

    def __getitem__(self, item):
        return self.__getattr__(item)
