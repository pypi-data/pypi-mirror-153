from importlib.resources import open_binary
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request

from djspoofer.remote.intoli import intoli_api


class GetProfilesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        with open_binary('djspoofer.tests.intoli.resources', 'user-agents.json.gz') as intoli_gz:

            mock_client.stream.return_value.__enter__.return_value = mock.Mock()
            mock_client.stream.return_value.__enter__.return_value.status_code = 200
            mock_client.stream.return_value.__enter__.return_value.iter_bytes.return_value = [
                intoli_gz.read()
            ]

        r_profiles = intoli_api.get_profiles(
            mock_client,
        )
        self.assertEquals(len(r_profiles.profiles), 5594)
        self.assertEquals(len(r_profiles.valid_profiles), 5515)
