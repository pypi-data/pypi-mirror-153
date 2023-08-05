import argparse

from django.core.management.base import BaseCommand


class ProxyCommand(BaseCommand):
    def handle(self, *args, **options):
        pass

    help = 'Test Proxies'

    def add_arguments(self, parser):
        parser.add_argument(
            "--proxy-disabled",
            action=argparse.BooleanOptionalAction,
            help="Proxy Disabled",
        )
        parser.add_argument(
            "--browser",
            type=str,
            required=False,
        )
