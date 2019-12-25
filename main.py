#!/usr/bin/env python3

import argparse
from console import Console


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for C code')
    parser.add_argument('target', metavar='<file>', help='C file to interpret')
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    arg = parser.parse_args()

    console = Console(arg.target, print_code=arg.verbose)
    console.init()
    console.interface.start()
