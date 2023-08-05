"""Check that a set of lines are included inside the content of a file."""

import argparse
import sys


def smart_quoted(value):
    return (
        f"'{value}'"
        if "'" not in value
        else (f'"{value}"' if '"' not in value else f"'{value}'")
    )


def file_check_lines(filename, expected_lines, quiet=False):
    with open(filename, encoding="utf-8") as f:
        lines = f.read().splitlines()

    expected_lines = [line.strip("\r\n") for line in expected_lines if line]
    if not expected_lines:
        sys.stderr.write("Any valid non empty expected line passed as argument\n")
        return 1

    retcode = 0
    for expected_line in expected_lines:
        if expected_line in lines:
            continue

        retcode = 1
        if not quiet:
            sys.stderr.write(
                f"Line {smart_quoted(expected_line)} not found in file {filename}\n"
            )

    return retcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    parser.add_argument(
        "lines_files", nargs="+", help="Lines and a filename to check for content"
    )
    args = parser.parse_args()

    return file_check_lines(
        args.lines_files[-1], args.lines_files[:-1], quiet=args.quiet
    )


if __name__ == "__main__":
    sys.exit(main())
