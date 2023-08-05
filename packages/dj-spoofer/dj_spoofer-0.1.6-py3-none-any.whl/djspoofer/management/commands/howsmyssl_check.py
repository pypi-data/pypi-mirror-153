from djstarter import utils

from djspoofer import clients, commands
from djspoofer.models import Fingerprint
from djspoofer.remote.howsmyssl import howsmyssl_api


class Command(commands.ProxyCommand):
    help = 'SSL Check'

    def handle(self, *args, **kwargs):
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=not kwargs['proxy_disabled']) as client:
                r_check = howsmyssl_api.ssl_check(client)
                self.stdout.write(utils.pretty_dict(r_check))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully got ssl check details'))
