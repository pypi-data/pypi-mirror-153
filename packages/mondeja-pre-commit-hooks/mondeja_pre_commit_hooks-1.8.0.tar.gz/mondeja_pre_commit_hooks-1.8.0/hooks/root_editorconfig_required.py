"""Script that checks if a repository has a root `.editorconfig` file
(``.editorconfig`` file with ``root=true`` defined).
"""

import argparse
import os
import sys


def check_root_editorconfig(quiet=False):
    """Check if the current directory has an '.editorconfig' file at the top
    path, and that this file has ``root = true`` set as directive.

    Parameters
    ----------

    quiet : bool, optional
      Enabled, don't print output to stderr when the script doesn't pass
      the checks.
    """
    if not os.path.isfile(".editorconfig"):
        if not quiet:
            sys.stderr.write("Missing '.editorconfig' file\n")
        return 1

    with open(".editorconfig") as f:
        content_lines = f.readlines()

    _root_true_found, _root_false_found = (False, False)
    _multiple_root_true_found = False
    for i, line in enumerate(content_lines):
        if line.strip().startswith("["):  # inside section header
            break

        stripped_line = line.strip().replace(" ", "")
        if stripped_line.startswith("root="):
            root_value = stripped_line.split("=")[1]

            if root_value == "false":
                _root_false_found = True
            elif root_value == "true":
                if _root_true_found:
                    _multiple_root_true_found = True
                _root_true_found = True
            else:
                if not quiet:
                    sys.stderr.write(
                        f"Invalid 'root' directive value '{root_value}' at"
                        f" '.editorconfig:{i + 1}'. Possible values are 'true'"
                        " and 'false'.\n"
                    )
                return 1

    if _root_false_found:
        if not quiet:
            sys.stderr.write(
                "Found 'root = false' in .editorconfig when expected to find"
                " 'root = true'.\n"
            )
        return 1

    if _multiple_root_true_found:
        if not quiet:
            sys.stderr.write(
                "Found multiple definitions of 'root = true' in .editorconfig\n"
            )
        return 1

    if not _root_true_found:
        if not quiet:
            sys.stderr.write(
                "Directive 'root = true' not found before section headers.\n"
            )
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    args = parser.parse_args()

    return check_root_editorconfig(quiet=args.quiet)


if __name__ == "__main__":
    exit(main())
