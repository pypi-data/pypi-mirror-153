from django.test import TestCase

from djspoofer.models import IntoliFingerprint


class ProfileTests(TestCase):
    """
    Profile Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.profile_data = {
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'viewport_height': 768,
            'viewport_width': 1024,
            'weight': .005,
        }

    def test_user_str(self):
        profile = IntoliFingerprint.objects.create(**self.profile_data)
        self.assertEqual(
            str(profile),
            ('IntoliFingerprint -> user_agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36, device_category: mobile, platform: US')
        )

    def test_is_desktop(self):
        profile = IntoliFingerprint.objects.create(**self.profile_data)
        self.assertFalse(profile.is_desktop)

    def test_is_mobile(self):
        profile = IntoliFingerprint.objects.create(**self.profile_data)
        self.assertTrue(profile.is_mobile)
