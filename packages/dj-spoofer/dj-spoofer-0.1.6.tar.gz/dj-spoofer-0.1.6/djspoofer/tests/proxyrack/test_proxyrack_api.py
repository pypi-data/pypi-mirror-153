import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer.remote.proxyrack import proxyrack_api, exceptions


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mocked_sleep = mock.patch('time.sleep', return_value=None).start()


class ActiveConnectionsTests(BaseTestCase):
    """
        Active Connections Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.proxyrack.resources', 'active_conns.json') as active_conns_json:
            cls.r_data = json.loads(active_conns_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.r_data
        )

        r_active_connections = proxyrack_api.active_connections(
            mock_client,
        )
        self.assertEquals(len(r_active_connections.connections), 2)

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.r_data
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.active_connections(
                mock_client,
            )


class APIKeyTests(BaseTestCase):
    """
        API Keys Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.proxyrack.resources', 'passwords.json') as passwords_json:
            cls.r_data = json.loads(passwords_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.r_data
        )

        r_temp = proxyrack_api.generate_temp_api_key(
            mock_client,
            expiration_seconds=60
        )
        self.assertEquals(r_temp.api_key, 'temp-bf3702-be83a4-0bbfc1-be7f58-62cfff')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.r_data
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.generate_temp_api_key(
                mock_client,
                expiration_seconds=60
            )


class ProxyCheckTests(BaseTestCase):
    """
        Test Proxy Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception

    @mock.patch.object(httpx, 'get')
    def test_ok(self, mock_get):
        mock_get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
        )

        is_valid_proxy = proxyrack_api.is_valid_proxy(proxies={'http://': 'http://example.com'})
        self.assertTrue(is_valid_proxy)
        self.assertEquals(mock_get.call_count, 1)

    @mock.patch.object(httpx, 'get')
    def test_407(self, mock_get):
        mock_get.return_value = Response(
            request=self.request,
            status_code=407,
        )

        self.assertFalse(proxyrack_api.is_valid_proxy(proxies={'http://': 'http://example.com'}))


class StatsTests(BaseTestCase):
    """
        Stats Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.proxyrack.resources', 'stats.json') as stats_json:
            cls.r_data = json.loads(stats_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.r_data
        )

        r_stats = proxyrack_api.stats(
            mock_client,
        )
        self.assertEquals(r_stats.thread_limit, 10000)

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.r_data
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.stats(
                mock_client,
            )


class IspsTests(BaseTestCase):
    """
        Isps Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.proxyrack.resources', 'us_isps.json') as isps_json:
            cls.r_data = json.loads(isps_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.r_data
        )

        r_isps = proxyrack_api.isps(
            mock_client,
            country='US'
        )
        self.assertEquals(len(r_isps.isps), 54)

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.r_data
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.isps(
                mock_client,
                country='US'
            )


class CountriesTests(BaseTestCase):
    """
        Countries Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.proxyrack.resources', 'countries.json') as countries_json:
            cls.r_data = json.loads(countries_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.r_data
        )

        r_countries = proxyrack_api.countries(
            mock_client,
            country='US'
        )
        self.assertEquals(len(r_countries.countries), 205)

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.r_data
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.countries(
                mock_client,
                country='US'
            )


class CitiesTests(BaseTestCase):
    """
        Cities Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.proxyrack.resources', 'cities.json') as cities_json:
            cls.r_data = json.loads(cities_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.r_data
        )

        r_cities = proxyrack_api.cities(
            mock_client,
            country='US'
        )
        self.assertEquals(len(r_cities.cities), 82)

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.r_data
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.cities(
                mock_client,
                country='US'
            )


class CountryIPCountTests(BaseTestCase):
    """
        Cities Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            text='152'
        )

        r_country_ip_count = proxyrack_api.country_ip_count(
            mock_client,
            country='US'
        )
        self.assertEquals(r_country_ip_count, '152')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            text='152'
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.country_ip_count(
                mock_client,
                country='US'
            )
