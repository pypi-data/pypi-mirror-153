# ISC License
#
# Copyright (c) 2019 David Caron
#
# Permission to use, copy, modify and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS-IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
requests Magpie authentication library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. This library
adds optional Magpie authentication support. Basic GET usage:

    >>> import requests
    >>> from requests_magpie import MagpieAuth
    >>> magpie_url = "https://www.example.com/magpie"
    >>> r = requests.get("http://example.org", auth=MagpieAuth(magpie_url, "username", "password"))

The entire `requests.api` should be supported.
"""

import requests
from requests import PreparedRequest
from requests.auth import AuthBase
from requests.cookies import merge_cookies
from requests.exceptions import RequestException

__version__ = '0.2.0'


class MagpieAuthenticationError(RequestException):
    """Magpie Authentication Error"""


class MagpieAuth(AuthBase):
    """Attaches Magpie Authentication to the given Request object."""

    def __init__(self, magpie_url, username, password, provider="ziggurat", cache=True, **request_kwargs):
        self.magpie_url = magpie_url
        self.username = username
        self.password = password
        self.provider = provider
        self.cache = cache
        self.request_kwargs = request_kwargs
        self._cookies = None

    def __call__(self, request: PreparedRequest):
        if self._cookies:
            merged_cookies = self._cookies
        else:
            signin_url = self.magpie_url.rstrip("/") + "/signin"
            data = {
                "user_name": self.username,
                "password": self.password,
                "provider_name": self.provider,
            }
            response = requests.post(signin_url, data=data, **self.request_kwargs)

            try:
                response.raise_for_status()
            except RequestException as e:
                raise MagpieAuthenticationError from e

            merged_cookies = merge_cookies(request._cookies, response.cookies)  # noqa
            if self.cache:
                self._cookies = merged_cookies

        request.prepare_cookies(merged_cookies)
        return request

    def __repr__(self):
        return f"<MagpieAuth url={self.magpie_url}, username={self.username}>"
