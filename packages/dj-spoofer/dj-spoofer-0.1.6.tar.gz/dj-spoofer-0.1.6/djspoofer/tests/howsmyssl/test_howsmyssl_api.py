import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer.remote.howsmyssl import howsmyssl_api


class GetProfilesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.howsmyssl.resources', 'ssl_check.json') as ssl_check_json:
            cls.ssl_check_json = json.loads(ssl_check_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.ssl_check_json
        )
        r_ssl_check = howsmyssl_api.ssl_check(
            mock_client,
        )

        self.assertTrue(r_ssl_check.session_ticket_supported)
        self.assertListEqual(r_ssl_check.given_cipher_suites, [
            "TLS_GREASE_IS_THE_WORD_3A",
            "TLS_AES_128_GCM_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_RSA_WITH_AES_128_CBC_SHA",
            "TLS_RSA_WITH_AES_256_CBC_SHA"
          ])
