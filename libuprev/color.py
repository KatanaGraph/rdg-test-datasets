HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARN = "\033[93m"
ERROR = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


def print_error(string: str):
    print("{}{}{}".format(ERROR, string, ENDC))


def print_warn(string: str):
    print("{}{}{}".format(WARN, string, ENDC))


def print_ok(string: str):
    print("{}{}{}".format(OKGREEN, string, ENDC))

def print_header(string: str):
    print("{}{}{}{}".format(HEADER, BOLD, string, ENDC))
