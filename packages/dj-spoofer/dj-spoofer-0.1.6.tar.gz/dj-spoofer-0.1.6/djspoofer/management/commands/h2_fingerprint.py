from djstarter import utils

from djspoofer import clients, commands
from djspoofer.models import Fingerprint
from djspoofer.remote.h2fingerprint import h2fingerprint_api


class Command(commands.ProxyCommand):
    help = 'Get H2 Fingerprint'

    def handle(self, *args, **kwargs):
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=not kwargs['proxy_disabled']) as client:
                r_h2 = h2fingerprint_api.get_h2_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_h2))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting H2 Fingerprint'))
