import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer.remote.incolumitas import exceptions, incolumitas_tcpip_api


class TCPIPFingerprintTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.incolumitas.resources', 'tcpip_fingerprint.json') as tcpip_fingerprint_json:
            cls.tcpip_fingerprint_json = json.loads(tcpip_fingerprint_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.tcpip_fingerprint_json
        )

        r_tcpip_fingerprint = incolumitas_tcpip_api.tcpip_fingerprint(
            mock_client,
        )
        self.assertEquals(r_tcpip_fingerprint.top_guess.os, 'macOS')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.tcpip_fingerprint_json
        )

        with self.assertRaises(exceptions.IncolumitasError):
            incolumitas_tcpip_api.tcpip_fingerprint(
                mock_client,
            )
