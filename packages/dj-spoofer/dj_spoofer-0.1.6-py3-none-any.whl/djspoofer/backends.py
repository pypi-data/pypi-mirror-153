import logging
from abc import ABC

logger = logging.getLogger(__name__)


class ProxyBackend(ABC):

    def get_proxy_url(self, fingerprint):
        raise NotImplemented  # pragma: no cover
