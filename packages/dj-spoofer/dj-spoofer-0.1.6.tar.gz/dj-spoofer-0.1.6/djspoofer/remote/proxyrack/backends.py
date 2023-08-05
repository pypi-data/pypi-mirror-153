import logging
import random
import uuid

from django.conf import settings
from djstarter import decorators
from httpx import Client

from djspoofer import backends, exceptions, utils
from djspoofer.models import IP, Proxy
from djspoofer.remote.proxyrack import proxyrack_api, utils as pr_utils

logger = logging.getLogger(__name__)


class ProxyRackProxyBackend(backends.ProxyBackend):
    def get_proxy_url(self, fingerprint):
        for ip in fingerprint.get_last_n_ips(count=3):
            logger.info(f'Testing prior IP Fingerprint: {ip}')
            proxy_url = self._build_proxy_url(proxyIp=ip.address)
            if self._is_valid_proxy(proxies=utils.proxy_dict(proxy_url)):
                logger.info(f'Found valid IP Fingerprint: {ip}')
                return proxy_url
        else:
            logger.info(f'{fingerprint}. No valid IP Fingerprints found. ')
            return self._new_proxy_url(fingerprint)   # Generate if no valid IP Fingerprints

    @decorators.retry(retry_exceptions=exceptions.ProxyConnectionFailed, tries=3, delay=0)
    def _new_proxy_url(self, fingerprint):
        logger.info(f'{fingerprint}. Generating new IP Fingerprint. ')
        proxy_url = self._test_proxy_url(fingerprint)
        proxies = utils.proxy_dict(proxy_url)
        if self._is_valid_proxy(proxies=proxies):
            self._create_ip_fingerprint(fingerprint, proxies)
            return proxy_url
        raise exceptions.ProxyConnectionFailed(f'{fingerprint}. Failed to get a new valid proxy')

    @staticmethod
    def _is_valid_proxy(proxies):
        return proxyrack_api.is_valid_proxy(proxies)

    @staticmethod
    def _create_ip_fingerprint(fingerprint, proxies):
        with Client(proxies=proxies) as client:
            r_stats = proxyrack_api.stats(client)
        ip_fingerprint = IP.objects.create(
            city=r_stats.ipinfo.city,
            country=r_stats.ipinfo.country,
            isp=r_stats.ipinfo.isp,
            address=r_stats.ipinfo.ip,
            fingerprint=fingerprint
        )
        fingerprint.add_ip(ip_fingerprint)
        logger.info(f'{ip_fingerprint}. Successfully created new ip fingerprint')

    def _test_proxy_url(self, fingerprint):
        geolocation = fingerprint.geolocation
        logger.info(f'{fingerprint}. Using Geolocation: {geolocation}')
        return self._build_proxy_url(
            osName=fingerprint.device_fingerprint.os,
            country=getattr(geolocation, 'country', self._weighted_proxy_country()),
            city=getattr(geolocation, 'city', None),
            # isp=getattr(geolocation, 'isp', None),    # Appears to be too restrictive
        )

    @staticmethod
    def _build_proxy_url(**kwargs):
        return pr_utils.ProxyBuilder(
            username=settings.PROXY_USERNAME,
            password=settings.PROXY_PASSWORD,
            netloc=Proxy.objects.get_rotating_proxy().url,
            timeoutSeconds=60,
            session=str(uuid.uuid4()),
            **kwargs
        ).http_url

    @staticmethod
    def _weighted_proxy_country():
        countries, weights = zip(*settings.PROXYRACK_COUNTRY_WEIGHTS)
        return random.choices(population=countries, weights=weights, k=1)[0]
