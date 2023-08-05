import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from djspoofer.remote.ja3er import exceptions, ja3er_api
from httpx import Request, Response, codes


class DetailsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.ja3er.resources', 'details.json') as details_json:
            cls.details_json = json.loads(details_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.details_json
        )

        r_details = ja3er_api.details(
            mock_client,
        )
        self.assertEquals(r_details.ssl_version, '771')
        self.assertEquals(
            r_details.ciphers,
            '4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53'
        )
        self.assertEquals(r_details.ssl_extensions, '0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21')
        self.assertEquals(r_details.elliptic_curve, '29-23-24')
        self.assertEquals(r_details.elliptic_curve_point_format, '0')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.details_json
        )

        with self.assertRaises(exceptions.Ja3erError):
            ja3er_api.details(
                mock_client,
            )


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.ja3er.resources', 'search.json') as search_json:
            cls.search_json = json.loads(search_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.search_json
        )

        r_search = ja3er_api.search(
            mock_client,
            ja3_hash='b32309a26951912be7dba376398abc3b'
        )

        self.assertEquals(len(r_search.stats), 3)

        stats_2 = r_search.stats[1]
        self.assertEquals(stats_2.user_agent, 'Go-http-client/1.1')

        comment_3 = r_search.comments[2]
        self.assertEquals(comment_3.comment, 'challenge accepted')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.search_json
        )

        with self.assertRaises(exceptions.Ja3erError):
            ja3er_api.search(
                mock_client,
                ja3_hash='b32309a26951912be7dba376398abc3b'
            )
