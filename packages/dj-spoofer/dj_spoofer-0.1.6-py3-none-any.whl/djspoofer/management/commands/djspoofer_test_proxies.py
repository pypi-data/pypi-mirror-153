import argparse

from djspoofer import clients, commands
from djspoofer.models import Fingerprint


class Command(commands.ProxyCommand):
    help = 'Test Proxies'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--urls",
            required=True,
            nargs='*',
            help="Target URLs for proxies",
        )
        parser.add_argument(
            "--display-output",
            action=argparse.BooleanOptionalAction,
            help="Display Output",
        )

    def handle(self, *args, **kwargs):
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=not kwargs['proxy_disabled']) as client:
                for url in kwargs['urls']:
                    r = client.get(url)
                    if kwargs['display_output']:
                        self.stdout.write(r.text)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))
