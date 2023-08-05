import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from djspoofer.remote.h2fingerprint import exceptions, h2fingerprint_api
from httpx import Request, Response, codes


class DetailsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.h2_fingerprint.resources', 'response.json') as response_json:
            cls.response_json = json.loads(response_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.response_json
        )

        r_response = h2fingerprint_api.get_h2_fingerprint(mock_client)

        self.assertEquals(r_response.fingerprint, '1:65536;3:1000;4:6291456;6:262144|15663105|1:1:0:256|m,a,s,p')
        self.assertEquals(r_response.settings_frame, '1:65536;3:1000;4:6291456;6:262144')
        self.assertEquals(r_response.window_frame, '15663105')
        self.assertEquals(r_response.header_priority_frame, '1:1:0:256')
        self.assertEquals(r_response.pseudo_headers, 'm,a,s,p')
        self.assertEquals(r_response.user_agent, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.response_json
        )

        with self.assertRaises(exceptions.H2Error):
            h2fingerprint_api.get_h2_fingerprint(
                mock_client,
            )
