#!/usr/bin/env python3

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for C code')
    parser.add_argument('target', metavar='<file>', help='C file to interpret')
    arg = parser.parse_args()

    with open(arg.target, "r") as f:
        code = f.read()
