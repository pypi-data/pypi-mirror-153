from django.test import TestCase

from djspoofer import const, exceptions
from djspoofer.models import DeviceFingerprint, H2Fingerprint, Fingerprint, Proxy


class FingerprintManagerTests(TestCase):
    """
    FingerprintManager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.desktop_device_fingerprint_data = {
            'browser': 'Chrome',
            'device_category': 'desktop',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }
        cls.mobile_device_fingerprint_data = {
            'browser': 'Safari',
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                           'Version/15.4 Safari/605.1.15'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_desktop_only(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Fingerprint.objects.random_desktop()

        new_fingerprint = Fingerprint.objects.create(device_fingerprint=DeviceFingerprint.objects.create(
            **self.desktop_device_fingerprint_data)
        )
        self.assertEquals(
            Fingerprint.objects.desktop_only(
                browser=new_fingerprint.device_fingerprint.browser,
                os=new_fingerprint.device_fingerprint.os,
            ).first(),
            new_fingerprint
        )

    def test_mobile_only(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Fingerprint.objects.random_mobile()

        new_fingerprint = Fingerprint.objects.create(device_fingerprint=DeviceFingerprint.objects.create(
            **self.mobile_device_fingerprint_data)
        )
        self.assertEquals(
            Fingerprint.objects.mobile_only(
                browser=new_fingerprint.device_fingerprint.browser,
                os=new_fingerprint.device_fingerprint.os,
            ).first(),
            new_fingerprint
        )

    def test_get_random_desktop_fingerprint(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Fingerprint.objects.random_desktop()

        Fingerprint.objects.create(device_fingerprint=DeviceFingerprint.objects.create(
            **self.desktop_device_fingerprint_data)
        )
        self.assertIsInstance(Fingerprint.objects.random_desktop(), Fingerprint)

    def test_get_random_mobile_fingerprint(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Fingerprint.objects.random_mobile()

        Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(
                **self.mobile_device_fingerprint_data
            )
        )
        self.assertIsInstance(Fingerprint.objects.random_mobile(), Fingerprint)


class H2FingerprintManagerTests(TestCase):
    """
    H2FingerprintManager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.h2_fingerprint_data = {
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

    def test_get_by_browser_info(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Fingerprint.objects.random_desktop()

        H2Fingerprint.objects.create(**self.h2_fingerprint_data)
        h2_fingerprint = H2Fingerprint.objects.get_by_browser_info(
            os='Windows',
            browser='Chrome',
            browser_major_version=78
        )
        self.assertIsNone(h2_fingerprint)
        h2_fingerprint = H2Fingerprint.objects.get_by_browser_info(
            os='Windows',
            browser='Chrome',
            browser_major_version=96
        )
        self.assertIsInstance(h2_fingerprint, H2Fingerprint)


class ProxyManagerTests(TestCase):
    """
    ProxyManager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.proxy_data = {
            'url': 'user123:password456@example.com:4582',
            'country': 'US',
            'city': 'dallas',
        }
        cls.proxy_data_2 = {
            'url': 'another123:password456@example.com:4582',
            'country': 'US',
            'city': 'dallas',
        }

    def test_get_rotating_proxy(self):
        Proxy.objects.create(**self.proxy_data)
        with self.assertRaises(exceptions.DJSpooferError):
            Proxy.objects.get_rotating_proxy()

        Proxy.objects.create(mode=const.ProxyModes.ROTATING.value, **self.proxy_data_2)
        self.assertIsNotNone(Proxy.objects.get_rotating_proxy())

    def test_get_sticky_proxy(self):
        Proxy.objects.create(**self.proxy_data)
        with self.assertRaises(exceptions.DJSpooferError):
            Proxy.objects.get_sticky_proxy()

        Proxy.objects.create(mode=const.ProxyModes.STICKY.value, **self.proxy_data_2)
        self.assertIsNotNone(Proxy.objects.get_sticky_proxy())

    def test_get_all_urls(self):
        Proxy.objects.create(**self.proxy_data)
        Proxy.objects.create(mode=const.ProxyModes.STICKY.value, **self.proxy_data_2)

        self.assertListEqual(
            sorted(list(Proxy.objects.get_all_urls())),
            sorted([self.proxy_data['url'], self.proxy_data_2['url']])
        )
