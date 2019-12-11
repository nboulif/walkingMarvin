
COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_PURPLE = "\033[35m"
COLOR_BLUE = "\033[34m"
COLOR_YELLOW = "\033[33m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_GREY = "\033[30m"

def warning(param):
    print(f'{COLOR_YELLOW}[WARNING] - {param}{COLOR_RESET}')

def debug(param):
    print(f'{COLOR_BLUE}[DEBUG] - {param}{COLOR_RESET}')

def info(param):
    print(f'{COLOR_WHITE}[INFO] {param}{COLOR_RESET}')

def error(param):
    print(f'{COLOR_RED}[ERROR] - {param}{COLOR_RESET}')

def critical(param):
    print(f'{COLOR_RED}[CRITICAL] - {param}{COLOR_RESET}')
