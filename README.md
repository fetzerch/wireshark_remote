[![Build Status](https://github.com/fetzerch/wireshark_remote/actions/workflows/check.yml/badge.svg)](https://github.com/fetzerch/wireshark_remote/actions/workflows/check.yml)
[![Coverage Status](https://coveralls.io/repos/github/fetzerch/wireshark_remote/badge.svg)](https://coveralls.io/github/fetzerch/wireshark_remote)
[![PyPI Version](https://img.shields.io/pypi/v/wireshark_remote.svg)](https://pypi.org/project/wireshark_remote)

# wireshark_remote - Initiate wireshark remote capture (SSH or AVM FRITZ!Box)

This project provides the `wireshark-ssh` and `wireshark-fritzbox` wrapper
scripts that simplify executing Wireshark to remotely capture network traffic.

## Installation

*wireshark_remote* (and its dependencies) can be installed from PyPI with:
`python -m pip install wireshark_remote`

In addition the following programs need to be available an in `PATH`.
The corresponding packages have to be installed through your distro's package
manager.

`wireshark-ssh` requires on the host:

* wireshark
* ssh

and on the remote machine (besides having an SSH server running):

* tcpdump
* sudo (optional)

`wireshark-fritzbox` requires on the host:

* wireshark
* wget

## Usage

### `wireshark-ssh`

```sh
Usage: wireshark-ssh.py [OPTIONS] HOST [EXPRESSION]...

  Launches wireshark locally and runs tcpdump on the remote [USER@]HOST via
  SSH. An optional tcpdump filter EXPRESSION allows to prefilter the captured
  packets.

Options:
  -i, --interface TEXT  The interface to capture from (default any).
  -s, --sudo            Run tcpdump via sudo.
  --help                Show this message and exit.
```

The following example shows how to remotely capture DNS network traffic on any
interface over SSH (tcpdump is executed with sudo on the remote host):

```sh
wireshark-ssh --sudo <user>@<host> port 53
```

### `wireshark-fritzbox`

```sh
Usage: wireshark-fritzbox.py [OPTIONS] [HOST]

  Launches wireshark locally and captures from the AVM FRITZ!Box webinterface.

Options:
  -i, --interface TEXT  The interface to capture from (default 3-0).
  -U, --username TEXT   [required]
  -P, --password TEXT   [required]
  --help                Show this message and exit.
```

The following example shows how to remotely capture all network traffic on the
*Routing Interface* (3-0) of the AVM FRITZ!Box on `fritz.box`:

```sh
wireshark-fritzbox -U <username> -P <password>
```

## License

This projected is licensed under the terms of the MIT license.
