"""wireshark_remote - Initiate wireshark remote capture (SSH or AVM FRITZ!Box)"""

# wireshark_remote - Initiate wireshark remote capture (SSH or AVM FRITZ!Box)
# Copyright 2021-2022 Christian Fetzer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import subprocess
import tempfile

import click

from .fritzbox_web import get_sid


def splituser(host, defaultuser=None):
    """splituser('user[:passwd]@host[:port]') --> 'user[:passwd]', 'host[:port]'.

    From deprecated urlib.parse.splituser().
    """
    user, delim, host = host.rpartition("@")
    return (user if delim else defaultuser), host


def build_filter_expression(parts):
    """Join list of expression parts with 'and' to a tcpdump filter expression"""
    parts = [
        part if isinstance(part, str) else " ".join(part) for part in parts if part
    ]
    if not parts:
        return ""
    return f"({ ') and ('.join(parts) })"


def run_wireshark(stdin):  # pragma: no cover
    """Run wireshark"""
    # Ensure wireshark doesn't leave temporary .pcapng files behind (when closed with CTRL-C)
    # by controlling the temporary directory it writes to.
    # Wireshark 3.7.0 introduces a --temp-path parameter. Until that is released, modify TMPDIR.
    with tempfile.TemporaryDirectory(prefix="wireshark_") as temp_dir:
        env = os.environ.copy()
        env["TMPDIR"] = temp_dir
        with subprocess.Popen(["wireshark", "-k", "-i", "-"], env=env, stdin=stdin):
            pass


@click.command()
@click.argument("host")
@click.argument("expression", nargs=-1)
@click.option(
    "-i",
    "--interface",
    default="any",
    help="The interface to capture from (default any).",
)
@click.option("-s", "--sudo", is_flag=True, help="Run tcpdump via sudo.")
def wireshark_ssh(host, expression, interface, sudo):  # pragma: no cover
    """Launches wireshark locally and runs tcpdump on the remote [USER@]HOST via
    SSH. An optional tcpdump filter EXPRESSION allows to prefilter the captured
    packets.
    """
    user, host = splituser(host, defaultuser="root")
    filter_expression = build_filter_expression([expression, "not port 25"])
    with subprocess.Popen(
        [
            "ssh",
            f"{user}@{host}",
            "sudo" if sudo else "",
            "tcpdump",
            f"--interface={interface}",
            "--snapshot-length=0",
            "--packet-buffered",
            f"'{filter_expression}'",
            "-w",
            "-",
        ],
        stdout=subprocess.PIPE,
    ) as p_ssh:
        run_wireshark(p_ssh.stdout)


@click.command()
@click.argument("host", default="fritz.box")
@click.option(
    "-i",
    "--interface",
    default="3-0",
    help="The interface to capture from (default 3-0).",
)
@click.option("-U", "--username", required=True)
@click.option("-P", "--password", required=True)
def wireshark_fritzbox(host, interface, username, password):  # pragma: no cover
    """Launches wireshark locally and captures from the AVM FRITZ!Box
    webinterface.
    """
    session_id = get_sid(f"http://{host}", username, password)
    with subprocess.Popen(
        [
            "wget",
            "-qO-",
            f"http://{host}/cgi-bin/capture_notimeout?"
            f"ifaceorminor={interface}&snaplen=&capture=Start&sid={session_id}",
        ],
        stdout=subprocess.PIPE,
    ) as p_ssh:
        run_wireshark(p_ssh.stdout)
