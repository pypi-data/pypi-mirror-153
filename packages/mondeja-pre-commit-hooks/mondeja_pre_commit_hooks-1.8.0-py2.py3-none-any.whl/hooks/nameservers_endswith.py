"""Script that checks if the nameservers of a domain ends with a defined string."""

import argparse
import sys

import dns.resolver


MAX_RETRY = 5


def nameservers_endswith(domain, nameserver, quiet=False, _retry=1):
    """Check that the nameservers of a domain endswith a strip after stripping
    it all newlines and points.

    Parameters
    ----------

    domain : str
      Domain whose nameserves will be checked.

    nameserver: str
      String that should match with the end of the string for the nameservers
      handlers of the domain. For example, passing ``cloudflare.com`` you
      can check if a domain is handled by Cloudflare.

    quiet : bool, optional
      Don't print the error in STDERR if a nameserver doesn't match.

    Returns
    -------

    bool : ``True`` if the nameservers match or ``False``.
    """
    response = True

    try:
        for ns in sorted(dns.resolver.resolve(domain, "NS")):
            ns_ = ns.to_text().strip().strip(".")
            if not ns_.endswith(nameserver):
                if not quiet:
                    sys.stderr.write(
                        f"Found invalid nameserver '{ns_}' for domain '{domain}'.\n"
                    )
                response = False
    except dns.exception.Timeout:
        if _retry > MAX_RETRY:
            if not quiet:
                sys.stderr.write(
                    "Maximum number of attempts retrieving nameserver DNS records.\n"
                )
            return False

        return nameservers_endswith(
            domain,
            nameserver,
            quiet=quiet,
            _retry=_retry + 1,
        )
    else:
        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    parser.add_argument(
        "-d",
        "-domain",
        "--domain",
        type=str,
        metavar="DOMAIN",
        required=True,
        default=None,
        dest="domain",
        help="Domain which nameservers will be checked.",
    )
    parser.add_argument(
        "-ns",
        "-nameserver",
        "--nameserver",
        type=str,
        metavar="NAMESERVER",
        required=True,
        default=None,
        dest="nameserver",
        help=(
            "End of the string that must match the nameservers handlers"
            " of the domain."
        ),
    )
    args = parser.parse_args()

    return (
        0 if nameservers_endswith(args.domain, args.nameserver, quiet=args.quiet) else 1
    )


if __name__ == "__main__":
    sys.exit(main())
