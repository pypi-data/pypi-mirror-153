from ssl import Options

from django.test import TestCase

from djspoofer.models import Geolocation, DeviceFingerprint, H2Fingerprint, TLSFingerprint, Fingerprint, IP, Proxy
from djspoofer.exceptions import DJSpooferError


class FingerprintTests(TestCase):
    """
    Fingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.device_fingerprint_data = {
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }
        cls.ip_fingerprint_data = {
            'city': 'Los Angeles',
            'country': 'US',
            'isp': 'Spectrum',
            'address': '194.60.86.250',
        }
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

    def test_str(self):
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        )
        self.assertEqual(str(fp), f'Fingerprint -> user_agent: {self.device_fingerprint_data["user_agent"]}')

    def test_ok(self):
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        )
        self.assertEquals(fp.tls_fingerprint.browser, fp.device_fingerprint.browser)

    def test_set_geolocation(self):
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        )
        geolocation = Geolocation.objects.create(city='Los Angeles')
        fp.set_geolocation(geolocation)
        self.assertEquals(fp.tls_fingerprint.browser, fp.device_fingerprint.browser)

    def test_get_first_n_ip_fingerprints(self):
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        )
        self.assertEquals(fp.get_last_n_ips(3).count(), 0)

        for _ in range(6):
            fp.add_ip(IP.objects.create(**self.ip_fingerprint_data))

        self.assertEquals(fp.get_last_n_ips(4).count(), 4)

    def test_add_ip_fingerprint(self):
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        )

        self.assertIsNone(fp.geolocation)

        ip_fingerprint = IP.objects.create(**self.ip_fingerprint_data)
        fp.add_ip(ip_fingerprint)

        self.assertEquals(fp.ip.all().count(), 1)
        self.assertEquals(fp.geolocation.isp, 'Spectrum')

    def test_h2_fingerprint(self):
        H2Fingerprint.objects.create(**self.h2_fingerprint_data)
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data),
        )
        self.assertIsInstance(fp.h2_fingerprint, H2Fingerprint)

    def test_no_h2_fingerprint(self):
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        )
        with self.assertRaises(DJSpooferError):
            _ = fp.h2_fingerprint

    def test_tls_fingerprint(self):
        fp = Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        )
        self.assertIsInstance(fp.tls_fingerprint, TLSFingerprint)


class IPTests(TestCase):
    """
    IP Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.ip_data = {
            'city': 'Dallas',
            'country': 'US',
            'isp': 'Spectrum',
            'address': '194.60.86.250',
        }
        cls.fingerprint_data = {
            'browser': 'Chrome',
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_str(self):
        ip_fingerprint = IP.objects.create(
            **self.ip_data,
        )
        self.assertEqual(str(ip_fingerprint), f'IP -> address: 194.60.86.250')


class H2FingerprintTests(TestCase):
    """
    H2Fingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.h2_fingerprint_data = {
            'os': 'Windows',
            'browser': 'Chrome',
            'browser_min_major_version': 95,
            'browser_max_major_version': 100,
            'header_table_size': 65536,
            'max_concurrent_streams': 1000,
            'initial_window_size': 6291456,
            'max_header_list_size': 262144,
            'psuedo_header_order': 'm,a,s,p',
            'window_update_increment': 15663105,
            'header_priority_stream_id': 1,
            'header_priority_exclusive_bit': 1,
            'header_priority_depends_on_id': 0,
            'header_priority_weight': 256
        }

    def test_str(self):
        h2_fp = H2Fingerprint.objects.create(**self.h2_fingerprint_data)
        self.assertEquals(
            str(h2_fp),
            f'H2Fingerprint -> hash: 1:65536;3:1000;4:6291456;6:262144|15663105|1:1:0:256|m,a,s,p'
        )


class DeviceFingerprintTests(TestCase):
    """
    DeviceFingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.device_fingerprint_data = {
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_str(self):
        d_fp = DeviceFingerprint.objects.create(**self.device_fingerprint_data)
        self.assertEquals(
            str(d_fp),
            (f'DeviceFingerprint -> user_agent: {d_fp.user_agent}, device_category: {d_fp.device_category}, '
             f'platform: {d_fp.platform}'))


class TLSFingerprintTests(TestCase):
    """
    TLSFingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.tls_fingerprint_data = {
            'browser': 'Chrome',
        }

    def test_ciphers(self):
        tls_fp = TLSFingerprint.objects.create(**self.tls_fingerprint_data)
        self.assertTrue(':' in tls_fp.ciphers)

    def test_extensions(self):
        tls_fp = TLSFingerprint.objects.create(**self.tls_fingerprint_data)
        self.assertEquals(type(tls_fp.extensions), int)

        tls_fp.extensions = int(Options.OP_NO_TICKET | Options.OP_NO_RENEGOTIATION | Options.OP_ENABLE_MIDDLEBOX_COMPAT)
        self.assertEquals(tls_fp.extensions, 1074806784)


class ProxyTests(TestCase):
    """
    Proxy Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.proxy_data = {
            'url': 'user123:password456@example.com:4582',
            'country': 'US',
            'city': 'dallas',
        }

    def test_str(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEqual(str(proxy), 'Proxy -> url: user123:password456@example.com:4582, mode: GENERAL')

    def test_is_on_cooldown(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertFalse(proxy.is_on_cooldown)

        proxy.set_last_used()
        self.assertTrue(proxy.is_on_cooldown)

    def test_set_last_used(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEquals(proxy.used_count, 0)
        self.assertIsNone(proxy.last_used)

        proxy.set_last_used()
        self.assertEquals(proxy.used_count, 1)
        self.assertIsNotNone(proxy.last_used)

    def test_http_url(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertTrue(proxy.http_url, 'http://user123:password456@example.com:4582')

    def test_https_url(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEquals(proxy.https_url, 'https://user123:password456@example.com:4582')

