# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, 2017 Red Hat, Inc.
# Red Hat Author: Patrick Uiterwijk <puiterwijk@redhat.com>
#
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Python-Requests AuthBase wrapping OpenIDCClient."""
import datetime

import jwcrypto.jwk
import jwcrypto.jwt
import requests.auth

from solidclient.utils.utils import make_random_string


class OpenIDCClientAuther(requests.auth.AuthBase):
    def __init__(self, oidcclient, scopes, new_token=True, keypair=None, logger=None):
        self.client = oidcclient
        self.scopes = scopes
        self.new_token = new_token
        self.keypair = keypair
        self.logger = logger

    def handle_response(self, response, **kwargs):
        if response.status_code in [401, 403]:
            new_token = self.client.report_token_issue()
            if not new_token:
                return response
            self._set_auth_headers(response.request, new_token)

            # Consume the content so we can reuse the connection
            response.raw.release_conn()

            r = response.connection.send(response.request)
            r.history.append(response)

            return r
        else:
            return response

    def __call__(self, request):
        # request.register_hook('response', self.handle_response)
        token = self.client.get_token(self.scopes,
                                      new_token=self.new_token)
        if token is None:
            raise RuntimeError('No token received')

        self._set_auth_headers(request, token)

        return request

    def _set_auth_headers(self, request, token):
        full_token = self._get_full_token_by_value(token)
        token_type = full_token['token_type']
        request.headers['Authorization'] = '%s %s' % (token_type, token)

        if token_type == 'DPoP':
            request.headers['DPoP'] = self._make_dpop_token(self.keypair, str(request.url), request.method)

    def _get_full_token_by_value(self, access_token_value):
        for uuid, token in self.client._cache.items():
            if token['access_token'] == access_token_value:
                return token

    @staticmethod
    def _make_dpop_token(keypair, uri, method):
        """
        Get a DPoP token
        :param keypair: JSON string representation of jwcrypto.jwk.JWK
        :param uri: URI to bind token to
        :param method: Method to bind token to
        :return: Serialized jwcrypto.jwt.JWT
        """
        key = jwcrypto.jwk.JWK.from_json(keypair) if type(keypair) == str else keypair
        jwt = jwcrypto.jwt.JWT(
            header={
                "typ": "dpop+jwt",
                "alg": "ES256",
                "jwk": key.export(private_key=False, as_dict=True)
            },
            claims={
                "jti": make_random_string(),
                "htm": method,
                "htu": uri,
                "iat": int(datetime.datetime.now().timestamp())
            })

        jwt.make_signed_token(key)

        return jwt.serialize()
