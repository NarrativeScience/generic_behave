"""Programmatic entrypoint to running behave from the command line"""
import os
import sys

from behave.__main__ import main as behave_main

if __name__ == "__main__":
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    try:
        exit_code = behave_main(sys.argv[1:])
    finally:
        os.chdir(cwd)
        sys.exit(exit_code)
