from django.core.management.base import BaseCommand

from djspoofer import utils
from djspoofer.models import Fingerprint, DeviceFingerprint
from djspoofer.models import IntoliFingerprint


class Command(BaseCommand):
    help = 'Create Desktop Fingerprints'

    def add_arguments(self, parser):
        parser.add_argument(
            "--num_to_create",
            required=True,
            type=int,
            help="Number of Fingerprints to Create",
        )

    def handle(self, *args, **kwargs):
        try:
            num_to_create = kwargs['num_to_create']
            self.create_fingerprints(num_to_create)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully created fingerprints'))

    @staticmethod
    def create_fingerprints(num_to_create):
        for i_fp in IntoliFingerprint.objects.weighted_n_desktop(count=num_to_create):
            ua_parser = utils.UserAgentParser(i_fp.user_agent)
            Fingerprint.objects.create(
                device_fingerprint=DeviceFingerprint.objects.create(
                    browser=ua_parser.browser,
                    browser_major_version=ua_parser.browser_major_version,
                    device_category=i_fp.device_category,
                    os=ua_parser.os,
                    platform=i_fp.platform,
                    screen_height=i_fp.screen_height,
                    screen_width=i_fp.screen_width,
                    user_agent=i_fp.user_agent,
                    viewport_height=i_fp.viewport_height,
                    viewport_width=i_fp.viewport_width,
                )
            )
