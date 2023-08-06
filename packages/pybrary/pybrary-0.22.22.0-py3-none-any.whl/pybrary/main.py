from sys import exit

from pybrary.commandline import parse_args
from pybrary import commands


def main():
    a, k = parse_args()
    f, *a = a
    try:
        cmd = getattr(commands, f)
        success, output = cmd(*a, **k)
    except Exception as x:
        success, output = False, str(x)
    if success:
        print(output)
    else:
        exit(f' ! {output}')
