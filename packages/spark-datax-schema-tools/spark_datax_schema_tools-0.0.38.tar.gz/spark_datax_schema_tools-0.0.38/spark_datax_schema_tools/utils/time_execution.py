import datetime
import time
from functools import wraps

from color_tools import cprint
from prettytable import PrettyTable


def get_stage(title, content):
    """This method is for use pretty table

    :title: String
    :content: String
    :return: prettyTable
    """
    bcolors = dict(HEADER='\033[95m',
                   OKBLUE='\033[94m',
                   OKGREEN='\033[90m',
                   WARNING='\033[93m',
                   FAIL='\033[91m',
                   ENDC='\033[0m',
                   BOLD='\033[1m',
                   UNDERLINE='\033[4m')

    t = PrettyTable()
    t.field_names = [f'{bcolors.get("OKBLUE")}:::: {title} ::::{bcolors.get("ENDC")}']
    t.add_row([f'{bcolors.get("BOLD")} {content} {bcolors.get("ENDC")}'])
    print(t)


def get_time_function_execution(function_to_execute):
    @wraps(function_to_execute)
    def compute_execution_time(*args, **kwargs):
        start_time = time.time()
        result = function_to_execute(*args, **kwargs)
        if result is not None:
            end_time = time.time()
            tmin, tsec = divmod(datetime.timedelta(seconds=end_time - start_time).total_seconds(), 60)
            title = f"Time Execution: "
            content = f"{tmin:.0f} minutes and {round(tsec, 2)} seconds."
            cprint(f'{title} {content}', 'yellow')
        return result

    return compute_execution_time
