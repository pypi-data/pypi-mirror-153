# ITS Private Cloud Command Line Interface ``vss-cli``

[![CI][build-img]](https://gitlab-ee.eis.utoronto.ca/vss/vss-cli/commits/master)
[![Coverage][coverage-img]](https://gitlab-ee.eis.utoronto.ca/vss/vss-cli/commits/master)
[![PyPI][pypi-img]](https://pypi.python.org/pypi/vss-cli)
[![PyPI version][pyver-img]](https://pypi.python.org/pypi/vss-cli)


The ITS Private Cloud Command-Line Interface ``vss-cli`` simplifies the interaction with the 
[ITS Private Cloud RESTful API][ITS Private Cloud RESTful API] to manage your virtual machines and other services.
<br>
<br>
[![asciicast](https://asciinema.org/a/RpP8lQBxjW75SaYtubHqerEp7.svg)](https://asciinema.org/a/JB2CT3GmfdFFUXEDxBV3xI0i0)

## Documentation

Package documentation is now available at [docs][docs].

## Installation

> Windows users, follow the installation instructions [Installing Python on Windows][Installing Python on Windows] and 
  add ``%USERPROFILE%\AppData\Roaming\Python\Python37\Scripts`` to ``PATH``  environment variable prior running [pip][pip].

The fastest way to install VSS CLI is to use [pip][pip]:

```bash
pip install vss-cli
```
If you are planning to interact with `vskey-stor` execute the following command

```bash
pip install vss-cli[stor]
```
The command will install ``webdavclient3`` package from PyPI and Linux operating systems require ``libxml2``.

> Windows users, please install ``windows-curses`` and ``vss-cli`` as follows: 
 ``pip install --user vss-cli windows-curses``.
        
If you have the VSS CLI installed and want to upgrade to the latest version
you can run:

```bash
pip install --upgrade vss-cli
```

This will install VSS CLI as well as all dependencies. You can also just [download the tarball][download the tarball].
Once you have the `vss-cli` directory structure on your workstation, you can just run:

```bash
cd path_to_vss-cli
python setup.py install
```

## Docker

If you do not have a Python setup you can try using ``vss-cli`` via a container using Docker.

```bash
docker run uofteis/vss-cli
```

[docker-vss-cli][docker/docker-vss-cli] is a helpful script to run the ``vss-cli`` within a 
docker container. Just download or move the file and update the environment variables if required, 
give execution permission and move it to your ``$PATH``:

```bash
curl https://gitlab-ee.eis.utoronto.ca/vss/vss-cli/raw/master/docker/docker-vss-cli > vss-cli
chmod +x vss-cli
``` 

## CLI Releases

The release notes for the VSS CLI can be found [CHANGELOG](CHANGELOG.md) in the gitlab repo.

## Getting Started

Before using VSS CLI, you need setup your VSS credentials. You can do this in a couple of ways:

* Configuration file
* Environment variables
* Command Line Input

The quickest way to get started is to run the ``vss-cli configure mk`` command:

```bash
vss-cli configure mk

Endpoint [https://cloud-api.eis.utoronto.ca]: 
Username: jm
Password: 
Repeat for confirmation: 

```

To use environment variables, set ``VSS_USER`` and ``VSS_USER_PASS`` or ``VSS_TOKEN``:

```bash
export VSS_USER=USER
export VSS_USER_PASS=superstrongpassword
# or
export VSS_TOKEN=JWT_TOKEN
```

For detailed information about the ``vss-cli`` configuration, please refer to the 
[official documentation site][official documentation site].

## JSON Parameter Input 

VSS CLI options vary from simple string, boolean or numeric values to
JSON data structures as input parameters on the command line.

For example, consider the following command to deploy a new virtual
machine from a given template and provide a guest operating system
specification to reconfigure hostname, domain, dns, ip, subnet
and gateway:

```bash
vss compute vm mk from-template --source c5916abb-def3-4d4d-8abe-2240b0a6c265 \
      --description 'New virtual machine' \
      --custom-spec '{"hostname": "fe1", "domain": "eis.utoronto.ca", "interfaces": [{"dhcp": true}]}'
```

## Auto-completion

Bash completion support is provided by [Click][Click] and will complete
sub commands and parameters. Sub commands are always listed whereas parameters
only if at least a dash has been provided. Example:

```bash
vss-cli compute <TAB><TAB>
account    compute    configure  request    stor       token

vss-cli -<TAB><TAB>
--config      --no-verbose  --output      --verbose     --version     -c            -o
```

Activating `bash` or `zsh` completion can be done by executing the following commands:

For `bash`:

```bash
source <(vss-cli completion bash)
```

For `zsh`:
```bash
    source <(vss-cli completion zsh)
```

For `fish`

```bash
_VSS_CLI_COMPLETE=fish_source vss-cli > ~/.config/fish/completions/vss-cli-complete.fish
```

If you do it from your `.bashrc` or `.zshrc` it is recommend to use the form below 
as that does not trigger a run of vss-cli itself.

For `bash`:

```bash
eval "$(_VSS_CLI_COMPLETE=bash_source vss-cli)"
```

For `zsh`:

```bash
eval "$(_VSS_CLI_COMPLETE=zsh_source vss-cli)"
```

For `fish`:

```bash
eval (env _VSS_CLI_COMPLETE=fish_source vss-cli)
```

## VSS Shell

The VSS CLI provides a REPL interactive shell with tab-completion, suggestions and
command history.

```bash
Usage: vss shell [OPTIONS]

  REPL interactive shell.

Options:
  -i, --history TEXT  File path to save history
  --help              Show this message and exit.

```
To enter the shell just execute vss shell and you will get the following welcome message:

```bash
    __   _____ ___
    \ \ / / __/ __|      API Endpoint: https://cloud-api.eis.utoronto.ca/v2
     \ V /\__ \__ \      Tab-completion & suggestions
      \_/ |___/___/      Prefix external commands with "!"
       CLI v20xx.0.0      History is saved: /Users/user/.vss-cli/history

    Exit shell with :exit, :q, :quit, ctrl+d

vss (cloud-api) > 
```

## Getting Help

We use GitLab issues for tracking bugs, enhancements and feature requests.
If it turns out that you may have found a bug, please [open a new issue][open a new issue].

```bash
vss-cli --help

Usage: vss-cli [OPTIONS] COMMAND [ARGS]...

  Command line interface for the ITS Private Cloud.

Options:
  -e, --endpoint TEXT             The Cloud API endpoint URL
  -c, --config TEXT               Configuration file
  -t, --token TEXT                The Bearer token for the VSS API.
  -u, --username TEXT             The API username for VSS API.
  -p, --password TEXT             The API password for VSS API.
  --timeout INTEGER               Timeout for network operations.
  -l, --loglevel LVL              Either CRITICAL, ERROR, WARNING, INFO or
                                  DEBUG
  -v, --verbose                   Enables verbose mode.
  --debug                         Enables debug mode.
  -x                              Print back traces when exception occurs.
  -o, --output [json|yaml|table|auto|ndjson]
                                  Output format (default: auto).
  --table-format TEXT             Which table format to use (default: simple)
  --columns TEXT                  Custom columns key=value list. Example:
                                  VM=moref,PROVISIONED=storage.provisionedGB
  --columns-width INTEGER         Truncates column values (0: auto, -1:
                                  disable).
  --wait / --no-wait              wait for request(s) to complete
  -n, --no-headers                When printing tables don't use headers
                                  (default: print headers)
  -s, --sort-by TEXT              Sort table by the jsonpath expression.
                                  Example: updated_on
  -w, --webdav-server TEXT        The Webdav server.
  --version                       Show the version and exit.
  --help                          Show this message and exit.


Commands:
  account     Manage your VSS account
  completion  Output shell completion code for the specified shell (bash or
              zsh or fish).
  compute     Manage VMs, networks, folders, etc.
  configure   Configure VSS-CLI options.
  key         Manage your SSH Public Keys.
  message     Manage VSS Messages.
  misc        Miscellaneous utilities.
  plugins     External plugins.
  raw         Make a raw call to the API
  request     Manage various requests
  service     ITS Service catalog.
  shell       REPL interactive shell.
  status      Check API Status.
  stor        Manage your VSS storage account.
  token       Manage access tokens
  upgrade     Upgrade VSS CLI and dependencies.


```

## Versioning

The `vss-cli` versions are tagged based on [Calendar Versioning][Calendar Versioning]. Versions available in the 
[tags section][tags section] or [PyPI package section][PyPI package section].


## Contributing
Refer to the [Contributing Guide][Contributing Guide] and [Contributors](CONTRIBUTORS.md) for details on our code 
of conduct and the process of submitting code to the repository.

## Changelog 📝

Refer to the [Changelog][Changelog] for details. 

[Calendar Versioning]: https://calver.org/
[tags section]: https://gitlab-ee.eis.utoronto.ca/vss/vss-cli/tags
[PyPI package section]: https://pypi.org/project/vss-cli/#history
[official documentation site]: https://eis.utoronto.ca/~vss/vss-cli/configure.html
[docs]: https://eis.utoronto.ca/~vss/vss-cli/
[Contributing Guide]: https://eis.utoronto.ca/~vss/vss-cli/development.html
[Changelog]: https://eis.utoronto.ca/~vss/vss-cli/changelog.html
[docker/docker-vss-cli]: https://eis.utoronto.ca/~vss/vss-cli/docker.html
[download the tarball]: https://pypi.python.org/pypi/vss-cli
[Click]: http://click.pocoo.org/6/
[Python Releases for Windows]: https://www.python.org/downloads/windows/
[pip]: http://www.pip-installer.org/en/latest/
[open a new issue]: https://gitlab-ee.eis.utoronto.ca/vss/vss-cli/issues/new
[build-img]: https://gitlab-ee.eis.utoronto.ca/vss/vss-cli/badges/master/pipeline.svg
[coverage-img]: https://gitlab-ee.eis.utoronto.ca/vss/vss-cli/badges/master/coverage.svg
[pypi-img]: https://img.shields.io/pypi/v/vss-cli.svg
[pyver-img]: https://img.shields.io/pypi/pyversions/vss-cli.svg
[docker-pulls-img]:  https://img.shields.io/docker/pulls/uofteis/vss-cli.svg
[docker-image]: https://hub.docker.com/r/uofteis/vss-cli/
[python-tabulate]: https://pypi.org/project/tabulate/
[ITS Private Cloud RESTful API]: https://vss-wiki.eis.utoronto.ca/display/API
[Pull Request #76]: https://github.com/click-contrib/click-repl/pull/76