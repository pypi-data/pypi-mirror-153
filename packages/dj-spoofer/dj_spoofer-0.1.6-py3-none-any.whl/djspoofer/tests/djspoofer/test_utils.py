from django.test import TestCase

from djspoofer import utils


class UtilTests(TestCase):
    """
    Utility Tests
    """

    def test_fake_profile(self):
        old_profile = utils.FakeProfile()
        profile = utils.FakeProfile()
        self.assertNotEquals(old_profile, profile)

        self.assertIn(profile.gender, ['M', 'F'])
        self.assertIn(profile.full_gender, ['MALE', 'FEMALE'])
        self.assertEquals(profile.full_name, f'{profile.first_name} {profile.last_name}')

        dob = profile.dob
        self.assertEquals(profile.dob_yyyymmdd, f'{dob.year}-{dob.month:02}-{dob.day:02}')
        self.assertTrue(profile.us_phone_number.startswith('+1'))
        self.assertEquals(len(profile.us_phone_number), 12)

    def test_ua_parser(self):
        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.82 Safari/537.36')
        ua_parser = utils.UserAgentParser(user_agent=user_agent)

        self.assertEquals(
            str(ua_parser),
            ("UserAgentParser -> {'user_agent': {'family': 'Chrome', 'major': '99', 'minor': '0', 'patch': '4844'}, 'os': {'family': 'Windows', 'major': '10', 'minor': None, 'patch': None, 'patch_minor': None}, 'device': {'family': 'Other', 'brand': None, 'model': None}, 'string': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}")
        )

        user_agent = ua_parser._user_agent
        self.assertEquals(user_agent.family, 'Chrome')
        self.assertEquals(user_agent.major, '99')
        self.assertEquals(user_agent.minor, '0')
        self.assertEquals(user_agent.patch, '4844')

        os = ua_parser._os
        self.assertEquals(os.family, 'Windows')
        self.assertEquals(os.major, '10')
        self.assertIsNone(os.minor)
        self.assertIsNone(os.patch)

        self.assertEquals(ua_parser.browser, 'Chrome')
        self.assertEquals(ua_parser.browser_major_version, '99')
        self.assertEquals(ua_parser.os, 'Windows')

    def test_h2_fingerprint_parser(self):
        parser = utils.H2HashParser('1:65536;2:1;3:1000;4:6291456;5:16384;6:262144|15663105|1:1:0:256|m,a,s,p')

        settings_frame = parser.settings_frame
        self.assertEquals(settings_frame.header_table_size, 65536)
        self.assertEquals(settings_frame.push_enabled, True)
        self.assertEquals(settings_frame.max_concurrent_streams, 1000)
        self.assertEquals(settings_frame.initial_window_size, 6291456)
        self.assertEquals(settings_frame.max_frame_size, 16384)
        self.assertEquals(settings_frame.max_header_list_size, 262144)

        windows_frame = parser.window_frame
        self.assertEquals(windows_frame, 15663105)

        priority_frame = parser.header_priority_flags
        self.assertEquals(priority_frame.stream_id, 1)
        self.assertEquals(priority_frame.is_exclusive_bit, 1)
        self.assertEquals(priority_frame.depends_on_id, 0)
        self.assertEquals(priority_frame.weight, 256)

    def test_h2_hash(self):
        h2_hash = '1:65536;3:1000;4:6291456;6:262144|15663105|1:1:0:256|m,a,s,p'
        h2_fingerprint = utils.h2_hash_to_h2_fingerprint(
            os='Windows',
            browser='Chrome',
            h2_hash=h2_hash,
            browser_min_major_version=50,
            browser_max_major_version=100
        )
        self.assertEquals(h2_fingerprint.browser, 'Chrome')
        self.assertEquals(h2_fingerprint.os, 'Windows')
        self.assertEquals(h2_fingerprint.enable_push, None)
        self.assertEquals(h2_fingerprint.initial_window_size, 6291456)
        self.assertEquals(h2_fingerprint.window_update_increment, 15663105)
        self.assertEquals(h2_fingerprint.header_priority_weight, 256)
