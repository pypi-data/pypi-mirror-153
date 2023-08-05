import datetime
import random
import logging

from django.db import models
from django.utils import timezone
from djstarter.models import BaseModel

from . import const, exceptions, managers, utils

logger = logging.getLogger(__name__)


class BaseFingerprint(BaseModel):
    browser = models.CharField(max_length=32)
    browser_min_major_version = models.IntegerField(default=0)
    browser_max_major_version = models.IntegerField(default=999)
    os = models.CharField(max_length=32)

    class Meta:
        abstract = True


class H2Fingerprint(BaseFingerprint):
    objects = managers.H2FingerprintManager()

    header_table_size = models.IntegerField(blank=True, null=True)
    enable_push = models.BooleanField(blank=True, null=True)
    max_concurrent_streams = models.IntegerField(blank=True, null=True)
    initial_window_size = models.IntegerField()
    max_frame_size = models.IntegerField(blank=True, null=True)
    max_header_list_size = models.IntegerField(blank=True, null=True)
    psuedo_header_order = models.TextField()

    window_update_increment = models.IntegerField()

    header_priority_stream_id = models.IntegerField()
    header_priority_exclusive_bit = models.IntegerField()
    header_priority_depends_on_id = models.IntegerField()
    header_priority_weight = models.IntegerField()

    priority_frames = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'djspoofer_h2_fingerprint'
        ordering = ['-created']
        app_label = 'djspoofer'

    def __str__(self):
        return f'H2Fingerprint -> hash: {self.hash}'

    @property
    def hash(self):
        return f'{self.settings_hash}|{self.window_update_increment}|{self.header_frames_hash}|{self.psuedo_header_order}'

    @property
    def settings_hash(self):
        table = [
            self.header_table_size,
            int(self.enable_push) if self.enable_push else None,
            self.max_concurrent_streams,
            self.initial_window_size,
            self.max_frame_size,
            self.max_header_list_size
        ]
        return ';'.join([f'{i+1}:{key}' for i, key in enumerate(table) if key])

    @property
    def header_frames_hash(self):
        return ':'.join([
            str(self.header_priority_stream_id),
            str(self.header_priority_exclusive_bit),
            str(self.header_priority_depends_on_id),
            str(self.header_priority_weight)
         ])


class TLSFingerprint(BaseFingerprint):
    objects = managers.TLSFingerprintManager()

    extensions = models.IntegerField()
    ciphers = models.TextField()

    class Meta:
        db_table = 'djspoofer_tls_fingerprint'
        ordering = ['-created']
        app_label = 'djspoofer'

        indexes = [
            models.Index(fields=['browser', ], name='tls_fp_browser'),
        ]

    def generate_chrome_desktop_cipher_str(self):
        grease_cipher = f'TLS_GREASE_IS_THE_WORD_{random.randint(1, 8)}A'
        return ':'.join(
            [grease_cipher] + [c for c in self.shuffled_ciphers(ciphers=const.ChromeDesktopCiphers, start_idx=4)]
        )

    def generate_firefox_desktop_cipher_str(self):
        return ':'.join([c for c in self.shuffled_ciphers(ciphers=const.FirefoxDesktopCiphers, start_idx=3)])

    DESKTOP_CLIENT_CIPHER_MAP = {
        'Chrome': generate_chrome_desktop_cipher_str,
        'Firefox': generate_firefox_desktop_cipher_str
    }

    @staticmethod
    def shuffled_ciphers(ciphers, start_idx=0, min_k=6):
        first_ciphers = ciphers[:start_idx]
        rem_ciphers = ciphers[start_idx:]
        k = random.randint(min_k, len(rem_ciphers))
        return first_ciphers + random.sample(rem_ciphers, k=k)

    @staticmethod
    def random_tls_extension_int(min_k=4):
        k = random.randint(min_k, len(const.TLS_EXTENSIONS))
        ext_val = 0
        for ext in random.sample(const.TLS_EXTENSIONS, k=k):
            ext_val |= ext
        return int(ext_val)

    def save(self, *args, **kwargs):
        if not self.ciphers:
            self.ciphers = self.DESKTOP_CLIENT_CIPHER_MAP[self.browser](self)
        if not self.extensions:
            self.extensions = self.random_tls_extension_int()
        super().save(*args, **kwargs)


class BaseDeviceFingerprint(BaseModel):
    browser = models.CharField(max_length=32)
    browser_major_version = models.IntegerField()
    device_category = models.CharField(max_length=32)
    os = models.CharField(max_length=32)
    platform = models.CharField(max_length=32)
    screen_height = models.IntegerField()
    screen_width = models.IntegerField()
    user_agent = models.TextField()
    viewport_height = models.IntegerField()
    viewport_width = models.IntegerField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not all([self.browser, self.browser_major_version, self.os]):
            ua_parser = utils.UserAgentParser(self.user_agent)
            self.browser = ua_parser.browser
            self.browser_major_version = ua_parser.browser_major_version
            self.os = ua_parser.os
        super().save(*args, **kwargs)


class DeviceFingerprint(BaseDeviceFingerprint):
    class Meta:
        db_table = 'djspoofer_device_fingerprint'
        app_label = 'djspoofer'

        indexes = [
            models.Index(fields=['browser', ], name='idx_device_fp_browser'),
            models.Index(fields=['device_category', ], name='idx_device_fp_device_category'),
            models.Index(fields=['platform', ], name='idx_device_fp_platform'),
        ]

    def __str__(self):
        return (f'DeviceFingerprint -> user_agent: {self.user_agent}, device_category: {self.device_category}, '
                f'platform: {self.platform}')


class IntoliFingerprint(BaseDeviceFingerprint):
    objects = managers.IntoliFingerprintManager()

    weight = models.DecimalField(max_digits=25, decimal_places=24)

    class Meta:
        db_table = 'djspoofer_intoli_fingerprint'
        ordering = ['-weight']
        app_label = 'djspoofer'

        indexes = [
            models.Index(fields=['browser', ], name='idx_intoli_fp_browser'),
            models.Index(fields=['device_category', ], name='idx_intoli_fp_device_category'),
            models.Index(fields=['os', ], name='idx_intoli_fp_os'),
            models.Index(fields=['platform', ], name='idx_intoli_fp_platform'),
        ]

    def __str__(self):
        return (f'IntoliFingerprint -> user_agent: {self.user_agent}, device_category: {self.device_category}, '
                f'platform: {self.platform}')

    @property
    def is_desktop(self):
        return self.device_category == 'desktop'

    @property
    def is_mobile(self):
        return self.device_category == 'mobile'


class Geolocation(BaseModel):
    objects = managers.GeolocationManager()

    city = models.CharField(max_length=64)
    country = models.CharField(max_length=2)
    isp = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'djspoofer_geolocation'
        ordering = ['-created']
        app_label = 'djspoofer'

    def __str__(self):
        return f'Geolocation -> city: {self.city}, country: {self.country}, isp: {self.isp}'


class IP(BaseModel):
    objects = managers.IPManager()

    city = models.CharField(max_length=64)
    country = models.CharField(max_length=2)
    isp = models.CharField(max_length=64)
    address = models.GenericIPAddressField()

    class Meta:
        db_table = 'djspoofer_ip'
        ordering = ['-created']
        app_label = 'djspoofer'

        indexes = [
            models.Index(fields=['city', ], name='ip_fp_city'),
            models.Index(fields=['country', ], name='ip_fp_country'),
            models.Index(fields=['isp', ], name='ip_fp_isp'),
        ]

    def __str__(self):
        return f'IP -> address: {self.address}'


class Fingerprint(BaseModel):
    objects = managers.FingerprintManager()

    device_fingerprint = models.ForeignKey(
        to=DeviceFingerprint,
        related_name='fingerprints',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    _h2_fingerprint = models.ForeignKey(
        to=H2Fingerprint,
        related_name='fingerprints',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    _tls_fingerprint = models.ForeignKey(
        to=TLSFingerprint,
        related_name='fingerprints',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    geolocation = models.ForeignKey(
        to=Geolocation,
        related_name='fingerprints',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    ip = models.ManyToManyField(IP)

    class Meta:
        db_table = 'djspoofer_fingerprint'
        ordering = ['-created']
        app_label = 'djspoofer'

    def __str__(self):
        return f'Fingerprint -> user_agent: {self.device_fingerprint.user_agent}'

    @property
    def h2_fingerprint(self):
        if not self._h2_fingerprint:
            new_h2_fingerprint = H2Fingerprint.objects.get_by_browser_info(
                os=self.device_fingerprint.os,
                browser=self.device_fingerprint.browser,
                browser_major_version=self.device_fingerprint.browser_major_version
            )
            if not new_h2_fingerprint:
                raise exceptions.DJSpooferError('No Available H2 Fingerprints. Did you run the djspoofer_init command?')
            self._h2_fingerprint = new_h2_fingerprint
            self.save()
        return self._h2_fingerprint

    @property
    def tls_fingerprint(self):
        if not self._tls_fingerprint:
            tls_fingerprint = TLSFingerprint.objects.create(browser=self.device_fingerprint.browser)
            if not tls_fingerprint:
                raise exceptions.DJSpooferError('No Available TLS Fingerprints. Did you run the djspoofer_init command?')
            self._tls_fingerprint = tls_fingerprint
            self.save()
        return self._tls_fingerprint

    def set_geolocation(self, geolocation):
        self.geolocation = geolocation
        self.save()

    def get_last_n_ips(self, count=3):
        return self.ip.all().order_by('-created')[:count]

    def add_ip(self, ip):
        self.ip.add(ip)
        if not self.geolocation:
            self.geolocation = Geolocation.objects.create(
                city=ip.city,
                country=ip.country,
                isp=ip.isp,
            )
            logger.info(f'{self}. Now using Geolocation: {self.geolocation}')
        self.save()


class Proxy(BaseModel):
    objects = managers.ProxyManager()

    url = models.TextField(blank=False)
    mode = models.IntegerField(default=const.ProxyModes.GENERAL.value, choices=const.ProxyModes.choices())
    country = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    last_used = models.DateTimeField(blank=True, null=True)
    used_count = models.IntegerField(default=0)
    cooldown = models.DurationField(default=datetime.timedelta(minutes=10))

    class Meta:
        db_table = 'djspoofer_proxy'
        ordering = ['url']
        app_label = 'djspoofer'

    def __str__(self):
        return f'Proxy -> url: {self.url}, mode: {self.pretty_mode}'

    @property
    def http_url(self):
        return f'http://{self.url}'

    @property
    def https_url(self):
        return f'https://{self.url}'

    @property
    def is_on_cooldown(self):
        if self.last_used:
            return self.last_used > timezone.now() - self.cooldown
        return False

    @property
    def pretty_mode(self):
        return self.get_mode_display()

    def set_last_used(self):
        self.last_used = timezone.now()
        self.used_count += 1
        self.save()
