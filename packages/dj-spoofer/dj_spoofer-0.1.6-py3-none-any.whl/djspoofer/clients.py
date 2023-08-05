import logging
from ssl import TLSVersion

import httpx
from django.conf import settings
from djstarter.clients import RetryClient

from djspoofer import exceptions, utils
from djspoofer.models import Fingerprint
from djspoofer.remote.proxyrack import backends

logger = logging.getLogger(__name__)


class DesktopClient(RetryClient, backends.ProxyRackProxyBackend):
    def __init__(self, fingerprint, proxy_enabled=True, *args, **kwargs):
        self._proxy_enabled = proxy_enabled
        self.fingerprint = fingerprint
        logger.info(f'Starting session with fingerprint: {self.fingerprint}')
        self.user_agent = self.fingerprint.device_fingerprint.user_agent
        super().__init__(
            headers=self.init_headers(),
            http2=True,
            proxies=self._get_proxies() if self._proxy_enabled else dict(),
            verify=self._get_ssl_context(),
            *args,
            **kwargs
        )

    def init_headers(self):
        return {
            # 'accept': 'application/json',
            'h2-fingerprint-id': self.fingerprint.h2_fingerprint.oid_str
        }

    def _get_proxies(self):
        proxy_url = settings.PROXY_URL or self.get_proxy_url(self.fingerprint)
        return utils.proxy_dict(proxy_url)

    def _get_ssl_context(self):
        tls_fingerprint = self.fingerprint.tls_fingerprint

        context = httpx.create_ssl_context(http2=True, verify=settings.SSL_VERIFY)
        context.minimum_version = TLSVersion.TLSv1_2
        context.set_ciphers(tls_fingerprint.ciphers)
        context.options = tls_fingerprint.extensions
        context.keylog_filename = settings.KEYLOG_FILENAME

        return context

    def send(self, *args, **kwargs):
        self.headers.pop('Accept-Encoding', None)
        self.headers.pop('Connection', None)
        return super().send(*args, **kwargs)


class DesktopChromeClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ua_parser = utils.UserAgentParser(self.user_agent)

    def init_headers(self):
        return super().init_headers() | {
            'user-agent': self.user_agent,
        }

    @property
    def sec_ch_headers(self):
        return {
            'sec-ch-ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': self.sec_ch_ua_mobile,
            'sec-ch-ua-platform': self.sec_ch_ua_platform,
        }

    @property
    def sec_ch_ua(self):
        version = self.ua_parser.browser_major_version
        return f'" Not;A Brand";v="99", "Google Chrome";v="{version}", "Chromium";v="{version}"'

    @property
    def sec_ch_ua_mobile(self):
        return '?0'

    @property
    def sec_ch_ua_platform(self):
        return f'"{self.fingerprint.device_fingerprint.os}"'


class DesktopFirefoxClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_headers(self):
        return super().init_headers() | {
            'User-Agent': self.user_agent,
        }


BROWSER_MAP = {
    'Chrome': DesktopChromeClient,
    'Firefox': DesktopFirefoxClient
}


def desktop_client(fingerprint=None, *args, **kwargs):
    fingerprint = fingerprint or Fingerprint.objects.random_desktop()
    browser = fingerprint.device_fingerprint.browser
    try:
        return BROWSER_MAP[browser](fingerprint=fingerprint, *args, **kwargs)
    except KeyError:
        raise exceptions.DJSpooferError(
            f'{fingerprint}, Unknown browser: {browser}. Available browsers: {list(BROWSER_MAP.keys())}'
        )
