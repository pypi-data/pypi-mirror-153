import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer.remote.incolumitas import exceptions, incolumitas_tls_api


class TLSFingerprintTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.incolumitas.resources', 'tls_fingerprint.json') as tcpip_fingerprint_json:
            cls.tls_fingerprint_json = json.loads(tcpip_fingerprint_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.tls_fingerprint_json
        )

        r_tls_fingerprint = incolumitas_tls_api.tls_fingerprint(
            mock_client,
        )
        self.assertEquals(r_tls_fingerprint.ciphers_length, 30)
        self.assertListEqual(
            r_tls_fingerprint.ec_point_formats,
            [
                "uncompressed",
                "ansiX962_compressed_prime",
                "ansiX962_compressed_char2"
            ]
        )

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.tls_fingerprint_json
        )

        with self.assertRaises(exceptions.IncolumitasError):
            incolumitas_tls_api.tls_fingerprint(
                mock_client,
            )
