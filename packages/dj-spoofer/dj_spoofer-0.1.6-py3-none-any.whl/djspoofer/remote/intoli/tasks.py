import logging

from djstarter import decorators
from httpx import Client

from djspoofer import const as s_const, utils as s_utils
from djspoofer.remote.intoli import intoli_api, const
from djspoofer.remote.intoli.exceptions import IntoliError
from djspoofer.models import IntoliFingerprint

logger = logging.getLogger(__name__)


@decorators.db_conn_close
def get_profiles(*args, **kwargs):
    GetProfiles(*args, **kwargs).start()


class GetProfiles:
    def __init__(self, *args, **kwargs):
        self.max_profiles = kwargs.get('max_profiles', const.MAX_PROFILES)

    def start(self):
        with Client() as client:
            r_profiles = intoli_api.get_profiles(client)

        old_oids = list(IntoliFingerprint.objects.all_oids())
        profiles = self.build_profiles(r_profiles)

        try:
            new_profiles = IntoliFingerprint.objects.bulk_create(profiles)
        except Exception as e:
            raise IntoliError(info=f'Error adding user agents: {str(e)}')
        else:
            logger.info(f'Max Profiles: {self.max_profiles}')
            logger.info(f'Created New Intoli Profiles: {len(new_profiles)}')
            logger.info(f'Deleted Old Intoli Profiles: {IntoliFingerprint.objects.bulk_delete(oids=old_oids)[0]}')

    def build_profiles(self, r_profiles):
        new_profiles = list()
        # TODO Use SUPPORTED_OS_BROWSER_MAP to filter profiles
        # Take the OS, and if the browser is in the list, store it
        for profile in self.filtered_profiles(r_profiles):
            ua_parser = s_utils.UserAgentParser(profile.user_agent)
            temp_profile = IntoliFingerprint(
                browser=ua_parser.browser,
                browser_major_version=ua_parser.browser_major_version,
                os=ua_parser.os,
                device_category=profile.device_category,
                platform=profile.platform,
                screen_height=profile.screen_height,
                screen_width=profile.screen_width,
                user_agent=profile.user_agent,
                viewport_height=profile.viewport_height,
                viewport_width=profile.viewport_width,
                weight=profile.weight,
            )
            new_profiles.append(temp_profile)
        return new_profiles

    def filtered_profiles(self, r_profiles):
        profiles = r_profiles.valid_profiles
        profiles = [p for p in profiles if p.browser in s_const.SUPPORTED_OS_BROWSER_MAP.get(p.os, list())]
        return profiles[:self.max_profiles]
