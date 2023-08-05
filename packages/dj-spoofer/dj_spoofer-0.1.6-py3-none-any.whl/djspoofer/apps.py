import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class DJSpooferConfig(AppConfig):
    name = 'djspoofer'
    verbose_name = 'DJ Spoofer App'

    def ready(self):
        from httpcore._sync import http2
        from djspoofer import connections

        # Monkey patching to allow for dynamic h2 settings frame
        http2.HTTP2Connection = connections.NewHTTP2Connection
        logger.debug('Monkey patched HTTP2Connection')
