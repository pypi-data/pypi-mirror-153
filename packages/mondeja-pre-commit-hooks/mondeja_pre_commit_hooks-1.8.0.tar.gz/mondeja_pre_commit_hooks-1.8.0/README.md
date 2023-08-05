# mondeja's pre-commit hooks

[![PyPI][pypi-version-badge-link]][pypi-link]
[![Python versions][pypi-pyversions-badge-link]][pypi-link]
[![License][license-image]][license-link]
[![Tests][tests-image]][tests-link]

## Example configuration

```yaml
- repo: https://github.com/mondeja/pre-commit-hooks
  rev: v1.8.0
  hooks:
    - id: dev-extras-required
    - id: root-editorconfig-required
      args:
        - -domain=my-web.xyz
    - id: cloudflare-nameservers
      args:
        - -domain=my-web.xyz
    - id: cloudflare-gh-pages-dns
      args:
        - -domain=my-web.xyz
        - -username=my_gh_username
    - id: file-check-lines
      files: ^MANIFEST.in$
      args:
        - include README.md
        - include LICENSE
```

## Hooks

### **`add-pre-commit-hook`**

Add a pre-commit hook to your configuration file if is not already defined.

#### Arguments

- `-repo=URL` (*str*) Repository of the new hook.
- `-rev=VERSION` (*str*) Version of the new hook.
- `-hook=ID` (*str*) Identifier of the new hook.

> See [repo-stream][repo-stream-link] if you're wondering why you would need
 to add a pre-commit hook from another hook.

### **`dev-extras-required`**

> - Support for `pyproject.toml` and `setup.py` files is limited to
 printing errors, automatic file rewriting is not performed.

Check if your development dependencies contains all other extras requirements.
If an extra requirement is defined in other extra group than your development
one, it will be added to your development extra dependencies group. If your
development group is not defined, it will be created.

This is useful if you want to execute `python -m pip install -e .[dev]` to
install all the optional requirements of the package, so if you add a new
requirement to another groups, it will be added to development requirements.

#### Arguments

- `-extra=NAME` (*str*): Name for your development requirements extra group
 (as default `dev`).
- `-setup-cfg=PATH` (*str*): Path to your `setup.cfg` file, mandatory if
 the extras requirements are defined in a `setup.cfg` file and this is located
 in another directory than the current one.
- `-pyproject-toml=PATH` (*str*): Path to your `pyproject.toml` file,
 mandatory if the extras requirements are defined in a `pyproject.toml` file
 and this is located in another directory than the current one.

### **`file-check-lines`**

Check that a set of lines are included in a file. The file path must
be passed in the `files` argument and only one can match against the
regex.

The positional arguments must be the lines to check for inclusion in
the file, without newlines characters. Empty lines and lines composed
by newlines characters will be ignored.

### **`nameservers-endswith`**

Check that the nameservers of a domain ends with a string or raise an error.
You can use it to check if a site like Clouflare is managing a domain using
`-nameserver=cloudflare.com`.

#### Arguments

- `-domain=DOMAIN` (*str*): Domain name whose nameservers will be checked.
- `-nameserver=NAMESERVER` (*str*): String to end the domain name servers in.

### **`cloudflare-nameservers`**

Check that [Cloudflare][cloudflare-link] is handling the nameservers of a
domain.

#### Arguments

- `-domain=DOMAIN` (*str*): Domain name whose nameservers will be checked.

### **`cloudflare-gh-pages-dns`**

Check that the DNS records of a [Cloudflare][cloudflare-link] site are
configured to serve a static website under [Github Pages][gh-pages-link].

> You must define the environment variable `CF_API_KEY` with your
[Cloudflare API key][cloudflare-apikey-link].

The required DNS records to make it pass are:

| Type | Name | Content |
| --- | --- | --- |
| A | {domain} | 185.199.108.153 |
| A | {domain} | 185.199.109.153 |
| A | {domain} | 185.199.110.153 |
| A | {domain} | 185.199.111.153 |
| CNAME | www | {username}.github.io |

#### Arguments

- `-domain=DOMAIN`: Domain managed by Cloudflare whose DNS records will be
 checked.
- `-username=USER`: Github username or organization under the Github Pages site
 is being served.

#### Environment variables

- `CF_API_KEY`: [Cloudflare API key][cloudflare-apikey-link] of the user that
 is managing the DNS records of the site using [Cloudflare][cloudflare-link].

### **`root-editorconfig-required`**

Check if your repository has an `.editorconfig` file and if this has a `root`
directive defined as `true` before section headers.

### **`wavelint`**

Check if your WAVE files have the correct number of channels, frame rate,
durations...

You need to install 

#### Arguments

- `-nchannels=N` (*int*): Number of channels that your sounds must have.
- `-sample-width=N` (*int*): Number of bytes that your sounds must have.
- `-frame-rate=N` (*int*): Sampling frequency that your sounds must have.
- `-nframes=N` (*int*): Exact number of frames that your sounds must have.
- `-comptype=TYPE` (*str*): Compression type that your sounds must have.
- `-compname=NAME` (*int*): Compression that your sounds must have.
- `-min-duration=TIME` (*float*): Minimum duration in seconds that your
 sounds must have.
- `-max-duration=TIME` (*float*): Maximum duration in seconds that your
 sounds must have.

## More hooks

- [mondeja/pre-commit-po-hooks][pre-commit-po-hooks-link]

[pypi-link]: https://pypi.org/project/mondeja_pre_commit_hooks
[pypi-version-badge-link]: https://img.shields.io/pypi/v/mondeja_pre_commit_hooks
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/mondeja_pre_commit_hooks
[license-image]: https://img.shields.io/pypi/l/mondeja_pre_commit_hooks?color=light-green
[license-link]: https://github.com/mondeja/pre-commit-po-hooks/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/pre-commit-hooks/CI?logo=github&label=tests
[tests-link]: https://github.com/mondeja/pre-commit-hooks/actions?query=workflow%CI

[cloudflare-link]: https://cloudflare.com
[cloudflare-apikey-link]: https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys
[gh-pages-link]: https://pages.github.com
[pre-commit-po-hooks-link]: https://github.com/mondeja/pre-commit-po-hooks
[repo-stream-link]: https://github.com/mondeja/repo-stream

