from django.core.management.base import BaseCommand

from djspoofer.models import Proxy


class Command(BaseCommand):
    help = 'Add Proxy'

    def add_arguments(self, parser):
        parser.add_argument(
            "--proxy-url",
            required=True,
            type=str,
            help="Set the proxy url",
        )

    def handle(self, *args, **kwargs):
        proxy_url = kwargs['proxy_url']
        Proxy.objects.create_rotating_proxy(url=proxy_url)
        self.stdout.write(self.style.MIGRATE_LABEL('Successfully Created rotating Proxy'))
