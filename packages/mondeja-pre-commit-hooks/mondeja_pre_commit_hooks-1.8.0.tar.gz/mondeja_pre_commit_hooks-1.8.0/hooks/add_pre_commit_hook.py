"""Add a pre-commit hook to a pre-commit configuration file, if this exists."""

import argparse
import os
import sys

import yaml


def repeated_definitions_of_repo_in_config(config, repo):
    """Check if there are multiple definitions of the same repository in a
    pre-commit configuration object.

    Parameters
    ----------

    config : dict
      Pre-commit configuration dictionary.

    repo : str
      Repository to check for multiple definitions.

    Returns
    -------

    bool : ``True`` if there are more than one definition of the passed
      repository in the configuration dictionary, ``False`` otherwise.
    """
    return len([_repo for _repo in config["repos"] if _repo["repo"] == repo]) > 1


def is_repo_in_config(config, repo, rev, hook_id):
    """Get if a repository is defined in a pre-commit configuration.

    Parameters
    ----------

    config : dict
      Pre-commit configuration dictionary.

    repo : str
      Repository to search.

    rev : str
      Repository tag revision.

    hook_id : Hook identifier.

    Returns
    -------

    dict : Information about if the repository and the hook have been found.
    """
    response = {"repo_found": False, "hook_found": False, "same_rev": False}
    for repo_ in config["repos"]:
        if repo_["repo"] == repo:
            response["repo_found"] = True
            response["hook_found"] = hook_id in [hook["id"] for hook in repo_["hooks"]]
            response["same_rev"] = repo_["rev"] == rev
            break
    return response


def add_pre_commit_hook(repo, rev, hook_id, quiet=False, dry_run=False):
    """Add a pre-commit hook configuration to a pre-commit configuration file.

    Parameters
    ----------

    repo : str
      Repository where the hook to add is defined.

    rev : str
      Hook's repository version.

    hook_id: str
      Hook identifier.

    quiet : bool, optional
      Don't print output to STDERR (only has effect with ``dry_run`` enabled).

    dry_run: bool, optional
      When enabled, only writes to STDERR the replacements that would be added,
      but are not done.

    Returns
    -------

    int: 1 if the pre-commit configuration file has been changed, 0 otherwise.
    """
    pre_commit_config_path = ".pre-commit-config.yaml"
    if not os.path.isfile(pre_commit_config_path):
        return 0

    with open(pre_commit_config_path) as f:
        config_content = f.read()
        config = yaml.safe_load(config_content)

    if "repos" not in config or not config["repos"]:
        return 0

    repo_in_config = is_repo_in_config(config, repo, rev, hook_id)
    if not repo_in_config["repo_found"]:
        _repo_indentation = 2
        config_lines = config_content.splitlines(keepends=True)
        for line in config_lines:
            if line.lstrip().startswith("- repo:"):
                _repo_indentation = line.index("-")
                break
        indent = " " * _repo_indentation

        new_lines = config_lines
        if not config_lines[-1].strip():
            new_lines = config_lines[:-1]
        if config_lines[-1][-1] != "\n":
            config_lines[-1] += "\n"
        new_lines.extend(
            [
                f"{indent}- repo: {repo}\n",
                f"{indent}  rev: {rev}\n",
                f"{indent}  hooks:\n",
                f"{indent}    - id: {hook_id}\n",
            ]
        )

        if dry_run:
            if not quiet:
                sys.stderr.write(
                    f"The hook '{hook_id}' with repo '{repo}' (rev: {rev})"
                    " would be added to '.pre-commit.config.yaml'\n"
                )
        else:
            with open(pre_commit_config_path, "w") as f:
                f.writelines(new_lines)

        return 1

    # repo in configuration multiple times
    if repeated_definitions_of_repo_in_config(config, repo):
        sys.stderr.write(
            f"Multiple definitions of repository '{repo}' in configuration"
            " file '.pre-commit-config.yaml'. You must determine manually one"
            " of them.\n"
        )
        return 1

    if not repo_in_config["hook_found"]:
        config_lines = config_content.splitlines(keepends=True)

        _inside_repo, _hooks_line, _hooks_indent = (False, None, None)
        _rev_line = None
        for i, line in enumerate(config_lines):
            if not _inside_repo:
                if line.lstrip().startswith("- repo:") and repo in line.replace(
                    "- repo:", ""
                ):
                    _inside_repo = True
            else:
                if _hooks_line is not None:
                    if _hooks_indent is None:
                        _hooks_indent = line.index("-") if "-" in line else None

                    if line.lstrip().startswith("- repo:"):
                        break
                else:
                    if line.lstrip().startswith("hooks:"):
                        _hooks_line = i
                    elif line.lstrip().startswith("rev:"):
                        _rev_line = i

        new_lines = []
        for n, line in enumerate(config_lines):
            if n == _rev_line and not repo_in_config["same_rev"]:
                new_lines.append(line.split(":")[0] + f": {rev}\n")
            else:
                if n == _hooks_line:
                    if not new_lines[-1].strip():
                        new_lines = new_lines[:-1]
                    new_lines.append(line)
                    new_lines.append(" " * _hooks_indent + f"- id: {hook_id}\n")
                else:
                    new_lines.append(line)

        if dry_run:
            if not quiet:
                sys.stderr.write(
                    f"The hook '{hook_id}' would be added to repo '{repo}'"
                    f" (rev: {rev})' at '.pre-commit.config.yaml'\n"
                )
        else:
            with open(pre_commit_config_path, "w") as f:
                f.writelines(new_lines)
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Don't do the rewriting, just writes errors to stderr.",
    )
    parser.add_argument(
        "-repo",
        "--repo",
        type=str,
        metavar="URL",
        required=True,
        dest="repo",
        help="Repository URL where the hook is defined.",
    )
    parser.add_argument(
        "-rev",
        "--rev",
        type=str,
        metavar="VERSION",
        required=True,
        dest="rev",
        help="Repository tag to fetch.",
    )
    parser.add_argument(
        "-id",
        "--id",
        type=str,
        metavar="HOOK_ID",
        required=True,
        dest="hook_id",
        help="Identifier of the hook to be added.",
    )

    args = parser.parse_args()

    exitcode = add_pre_commit_hook(
        args.repo,
        args.rev,
        args.hook_id,
    )

    return exitcode


if __name__ == "__main__":
    exit(main())
