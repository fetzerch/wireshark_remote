"""Tests fo wireshark_remote"""

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

from wireshark_remote import splituser, build_filter_expression


def test_splituser():
    """Tests splituser function"""
    assert splituser("host") == (None, "host")
    assert splituser("user@host") == ("user", "host")
    assert splituser("user:pass@host:port") == ("user:pass", "host:port")
    assert splituser("host", defaultuser="root") == ("root", "host")


def test_build_filter_expression():
    """Tests building a tcpdump filter expression"""
    assert build_filter_expression([()]) == ""
    assert build_filter_expression([(), "not port 25"]) == "(not port 25)"
    assert (
        build_filter_expression([("not", "port", "25"), "not port 22"])
        == "(not port 25) and (not port 22)"
    )
