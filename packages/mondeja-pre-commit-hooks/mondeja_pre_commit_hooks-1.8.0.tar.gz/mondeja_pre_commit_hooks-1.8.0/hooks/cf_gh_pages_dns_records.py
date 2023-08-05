"""Script that checks that a cutomized domain has the minimal DNS records
configured into a Cloudflare zone to make it work with Github Pages:

RECORD    Name        Value
A         {domain}    185.199.108.153
A         {domain}    185.199.109.153
A         {domain}    185.199.110.153
A         {domain}    185.199.111.153
CNAME     www         {username}.github.io
"""

import argparse
import os
import sys

import CloudFlare


EXPECTED_A_RECORDS = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
]


def check_cloudflare_gh_pages_dns_records(
    domain,
    username,
    quiet=False,
):
    """Check if the DNS records A and CNAME of a customized domain are properly
    configured to work with Github Pages, managed from Cloudflare.

    Parameters
    ----------

    domain : str
      Domain managed by Cloudflare whose DNS records will be checked.

    username : str
      Github username or organization that is serving the page in their account.

    quiet : bool, optional
      Don't write error messages to STDERR, just exit with proper error code.

    Returns
    -------

    bool : ``True`` if the DNS records are properly configured or ``False``.
    """
    if not os.environ.get("CF_API_KEY"):
        sys.stderr.write(
            "You must configure the environment variable 'CF_API_KEY' with a"
            " Cloudflare API key.\n"
        )
        return False

    # get domain from Cloudflare (named "zone" by CF API)
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params={"name": domain})

    if not zones:
        sys.stderr.write(
            f"The domain '{domain}' was not found being managed by your"
            " Cloudflare account.\n"
        )
        return False

    # get DNS records configured for the domain
    zone_id = zones[0]["id"]
    dns_records = cf.zones.dns_records.get(zone_id)

    # filter "A" records
    a_records_found, cname_records_found = ([], [])

    for record in dns_records:
        if record["type"] == "A":
            a_records_found.append(record)
        elif record["type"] == "CNAME":
            cname_records_found.append(record)

    response = True

    # check A DNS record
    for expected_a_record in EXPECTED_A_RECORDS:
        _a_record_found = False
        for record in a_records_found:
            if record["content"] == expected_a_record:
                _a_record_found = True
                break

        if not _a_record_found:
            if not quiet:
                sys.stderr.write(
                    f"Expected A record with value '{expected_a_record}' in DNS"
                    f" configuration for domain '{domain}' but not found.\n"
                )
            response = False
    if not response and not quiet:
        sys.stderr.write(
            "Github pages must be configured using the next four A records:\n"
            + "\n".join(["- " + record for record in EXPECTED_A_RECORDS])
            + "\n\n"
            "Next records found:\n"
            + "\n".join(["- " + record["content"] for record in a_records_found])
            + "\n"
        )

    # check CNAME DNS record
    _cname_record_found, expected_cname_content = (False, f"{username}.github.io")
    for record in cname_records_found:
        if record["content"] == expected_cname_content:
            _cname_record_found = True
            break
    if not _cname_record_found:
        if not quiet:
            sys.stderr.write(
                f"Expected CNAME DNS record with value '{expected_cname_content}'"
                f" but not found for domain '{domain}'.\n"
            )
        response = False

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
        help="Domain managed by Cloudflare whose DNS configuration will be checked.",
    )
    parser.add_argument(
        "-u",
        "-username",
        "--username",
        "--github-username",
        type=str,
        metavar="USERNAME",
        required=True,
        default=None,
        dest="username",
        help=(
            "Github username or organization that is serving the page in their"
            " repository."
        ),
    )
    args = parser.parse_args()

    return (
        0
        if check_cloudflare_gh_pages_dns_records(
            args.domain,
            args.username,
            quiet=args.quiet,
        )
        else 1
    )


if __name__ == "__main__":
    sys.exit(main())
