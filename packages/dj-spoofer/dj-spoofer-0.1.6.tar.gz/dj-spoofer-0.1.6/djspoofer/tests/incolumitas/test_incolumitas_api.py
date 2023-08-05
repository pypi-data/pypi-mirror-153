import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer.remote.incolumitas import exceptions, incolumitas_api


class IPFingerprintTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.incolumitas.resources', 'ip_fingerprint.json') as ip_fingerprint_json:
            cls.ip_fingerprint_json = json.loads(ip_fingerprint_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.ip_fingerprint_json
        )

        r_ip_fingerprint = incolumitas_api.ip_fingerprint(
            mock_client,
            ip_addr='76.187.119.132'
        )
        self.assertEquals(r_ip_fingerprint.ip, '76.187.119.132')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.ip_fingerprint_json
        )

        with self.assertRaises(exceptions.IncolumitasError):
            incolumitas_api.ip_fingerprint(
                mock_client,
            )
