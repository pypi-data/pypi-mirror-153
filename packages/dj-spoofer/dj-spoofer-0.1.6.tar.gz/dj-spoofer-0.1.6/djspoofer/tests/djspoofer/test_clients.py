import json
from importlib.resources import open_text
from unittest import mock

from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer import clients, utils
from djspoofer.models import Fingerprint, DeviceFingerprint, H2Fingerprint, IP, Proxy, Geolocation
from djspoofer.remote.proxyrack import proxyrack_api


class DesktopChromeClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.proxy = Proxy.objects.create_rotating_proxy(
            url='test123:5000',
        )
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        device_fingerprint_data = {
            'device_category': 'desktop',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': user_agent,
            'viewport_height': 768,
            'viewport_width': 1024
        }
        h2_fingerprint_data = {
            'os': 'Windows',
            'browser': 'Chrome',
            'browser_min_major_version': 95,
            'browser_max_major_version': 100,
            'header_table_size': 65536,
            'enable_push': True,
            'max_concurrent_streams': 1000,
            'initial_window_size': 6291456,
            'max_frame_size': 16384,
            'max_header_list_size': 262144,
            'psuedo_header_order': 'm,a,s,p',
            'window_update_increment': 15663105,
            'header_priority_stream_id': 1,
            'header_priority_exclusive_bit': 1,
            'header_priority_depends_on_id': 0,
            'header_priority_weight': 256
        }
        cls.geo_location_data = {
            'city': 'Los Angeles',
            'country': 'US',
            'isp': 'Spectrum',
        }
        cls.ip_data = {
            'city': 'Dallas',
            'country': 'US',
            'isp': 'Spectrum',
            'address': '194.60.86.250',
        }
        cls.fingerprint = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**device_fingerprint_data),
            _h2_fingerprint=H2Fingerprint.objects.create(**h2_fingerprint_data),
        )
        with open_text('djspoofer.tests.proxyrack.resources', 'stats.json') as stats_json:
            cls.r_stats_data = proxyrack_api.StatsResponse(json.loads(stats_json.read()))

    @mock.patch.object(proxyrack_api, 'stats')
    @mock.patch.object(proxyrack_api, 'is_valid_proxy')
    @mock.patch.object(clients.DesktopChromeClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send, mock_is_valid_proxy, mock_stats):
        mock_sd_send.return_value = Response(
            request=Request(url='', method=''),
            status_code=codes.OK,
            text='ok'
        )
        mock_is_valid_proxy.return_value = True
        mock_stats.return_value = self.r_stats_data

        self.fingerprint.add_ip(IP.objects.create(**self.ip_data))

        with clients.DesktopChromeClient(fingerprint=self.fingerprint) as chrome_client:
            chrome_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)
            self.assertEquals(
                chrome_client.sec_ch_ua,
                '" Not;A Brand";v="99", "Google Chrome";v="99", "Chromium";v="99"'
            )
            self.assertEquals(chrome_client.sec_ch_ua_mobile, '?0')
            self.assertEquals(chrome_client.sec_ch_ua_platform, '"Windows"')

    @mock.patch.object(proxyrack_api, 'stats')
    @mock.patch.object(proxyrack_api, 'is_valid_proxy')
    @mock.patch.object(clients.DesktopChromeClient, '_send_handling_auth')
    def test_fingerprint_with_geolocation_no_ips(self, mock_sd_send, mock_is_valid_proxy, mock_stats):
        mock_sd_send.return_value = Response(
            request=Request(url='', method=''),
            status_code=codes.OK,
            text='ok'
        )
        mock_is_valid_proxy.return_value = True
        mock_stats.return_value = self.r_stats_data

        self.fingerprint.set_geolocation(Geolocation.objects.create(**self.geo_location_data))

        with clients.DesktopChromeClient(fingerprint=self.fingerprint) as chrome_client:
            chrome_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)
            self.assertEquals(
                chrome_client.sec_ch_ua,
                '" Not;A Brand";v="99", "Google Chrome";v="99", "Chromium";v="99"'
            )
            self.assertEquals(chrome_client.sec_ch_ua_mobile, '?0')
            self.assertEquals(chrome_client.sec_ch_ua_platform, '"Windows"')


class DesktopFirefoxClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.proxy = Proxy.objects.create_rotating_proxy(
            url='test123:5000',
        )
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        device_fingerprint_data = {
            'device_category': 'desktop',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': user_agent,
            'viewport_height': 768,
            'viewport_width': 1024
        }
        h2_fingerprint_data = {
            'os': 'Windows',
            'browser': 'Chrome',
            'browser_min_major_version': 95,
            'browser_max_major_version': 100,
            'header_table_size': 65536,
            'enable_push': True,
            'max_concurrent_streams': 1000,
            'initial_window_size': 6291456,
            'max_frame_size': 16384,
            'max_header_list_size': 262144,
            'psuedo_header_order': 'm,a,s,p',
            'window_update_increment': 15663105,
            'header_priority_stream_id': 1,
            'header_priority_exclusive_bit': True,
            'header_priority_depends_on_id': 0,
            'header_priority_weight': 256
        }
        cls.fingerprint = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**device_fingerprint_data),
            _h2_fingerprint=H2Fingerprint.objects.create(**h2_fingerprint_data)
        )
        with open_text('djspoofer.tests.proxyrack.resources', 'stats.json') as stats_json:
            cls.r_stats_data = proxyrack_api.StatsResponse(json.loads(stats_json.read()))

    @mock.patch.object(proxyrack_api, 'stats')
    @mock.patch.object(proxyrack_api, 'is_valid_proxy')
    @mock.patch.object(clients.DesktopFirefoxClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send, mock_is_valid_proxy, mock_stats):
        mock_sd_send.return_value = Response(
            request=Request(url='', method=''),
            status_code=codes.OK,
            text='ok'
        )
        mock_is_valid_proxy.return_value = True
        mock_stats.return_value = self.r_stats_data

        with clients.DesktopFirefoxClient(fingerprint=self.fingerprint) as sd_client:
            sd_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)


