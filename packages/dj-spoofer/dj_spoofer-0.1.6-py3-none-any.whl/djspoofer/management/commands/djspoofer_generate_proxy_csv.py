import argparse
import uuid

from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer import const
from djspoofer.models import Proxy


class Command(BaseCommand):
    help = 'Generate Proxy CSV'

    PROXY_FIELDS = ['oid', 'url', 'mode', 'country', 'city']

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            type=str,
            help="Target URL for proxies",
        )

        parser.add_argument(
            "--port-start",
            required=True,
            type=int,
            help="Proxy port start range",
        )
        parser.add_argument(
            "--port-end",
            required=True,
            type=int,
            help="Proxy port end range",
        )
        parser.add_argument(
            "--credentials",
            type=str,
            help="Proxy credentials",
        )
        parser.add_argument(
            "--proxy-mode",
            default=const.ProxyModes.STICKY.value,
            type=int,
            help="Proxy Mode",
        )
        parser.add_argument(
            "--load-proxies",
            action=argparse.BooleanOptionalAction,
            help="Load Proxies Into Database",
        )
        parser.add_argument(
            "--country",
            type=str,
            default='',
            help="Proxy Country",
        )

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        port_start = kwargs['port_start']
        port_end = kwargs['port_end']
        proxy_mode = kwargs['proxy_mode']
        credentials = kwargs['credentials']
        load_proxies = kwargs['load_proxies']
        country = kwargs['country']

        proxies = list()
        self.stdout.write(self.style.MIGRATE_LABEL(','.join(self.PROXY_FIELDS)))
        try:
            for port in range(port_start, port_end):
                columns = [
                    uuid.uuid4(),
                    self.build_proxy_str(url, port=port, credentials=credentials),
                    proxy_mode,
                    country,
                    ''
                ]
                proxies.append(self.build_proxy(columns))
                row = ','.join(str(c) for c in columns)
                self.stdout.write(self.style.MIGRATE_LABEL(row))
            if load_proxies:
                Proxy.objects.bulk_create(proxies)
                self.stdout.write(self.style.MIGRATE_LABEL(utils.eye_catcher_line('Successfully loaded proxies')))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(utils.eye_catcher_line('Successfully generated proxy csv')))

    @staticmethod
    def build_proxy(columns):
        return Proxy(
            oid=columns[0],
            url=columns[1],
            mode=columns[2],
            country=columns[3],
            city=columns[4]
        )

    @staticmethod
    def build_proxy_str(url, port, credentials=None):
        proxy_str = f'{url}:{port}'
        if credentials:
            proxy_str = f'{credentials}@{proxy_str}'
        return proxy_str
