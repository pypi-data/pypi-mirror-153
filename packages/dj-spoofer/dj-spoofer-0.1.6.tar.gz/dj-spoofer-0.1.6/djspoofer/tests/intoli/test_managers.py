from django.test import TestCase

from djspoofer.remote.intoli import exceptions
from djspoofer.models import IntoliFingerprint


class ProfileManagerTests(TestCase):
    """
    ProfileManager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.profile_data = {
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'viewport_height': 768,
            'viewport_width': 1024,
            'weight': .005,
        }

    def test_all_oids(self):
        profile = IntoliFingerprint.objects.create(device_category='desktop', **self.profile_data)

        self.assertEquals(list(IntoliFingerprint.objects.all_oids()), [profile.oid])

    def test_all_user_agents(self):
        IntoliFingerprint.objects.create(**self.profile_data)

        new_data = self.profile_data.copy()
        new_data['user_agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        IntoliFingerprint.objects.create(**new_data)

        user_agents = IntoliFingerprint.objects.all_user_agents()

        self.assertListEqual(
            list(user_agents),
            [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
            ]
        )

    def test_random_desktop_chrome_profile(self):
        with self.assertRaises(exceptions.IntoliError):
            IntoliFingerprint.objects.random_desktop()

        IntoliFingerprint.objects.create(browser='Chrome', device_category='desktop', os='Windows', **self.profile_data)

        profile = IntoliFingerprint.objects.random_desktop()

        self.assertEquals(profile.user_agent, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')

    def test_random_mobile_profile(self):
        with self.assertRaises(exceptions.IntoliError):
            IntoliFingerprint.objects.random_mobile()

        IntoliFingerprint.objects.create(device_category='mobile', **self.profile_data)

        profile = IntoliFingerprint.objects.random_mobile()

        self.assertEquals(profile.user_agent, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')

    def test_weighted_desktop_chrome_user_agent(self):
        with self.assertRaises(exceptions.IntoliError):
            IntoliFingerprint.objects.weighted_n_desktop()

        IntoliFingerprint.objects.create(browser='Chrome', device_category='desktop', os='Windows', **self.profile_data)

        profile = IntoliFingerprint.objects.weighted_n_desktop()[0]

        self.assertEquals(profile.user_agent, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')

    def test_weighted_mobile_user_agent(self):
        with self.assertRaises(exceptions.IntoliError):
            IntoliFingerprint.objects.weighted_n_mobile()

        IntoliFingerprint.objects.create(device_category='mobile', **self.profile_data)

        profile = IntoliFingerprint.objects.weighted_n_mobile()[0]

        self.assertEquals(profile.user_agent, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')

    def test_bulk_delete(self):
        profile = IntoliFingerprint.objects.create(device_category='desktop', os='Linux', **self.profile_data)

        IntoliFingerprint.objects.bulk_delete(oids=[profile.oid])

        with self.assertRaises(IntoliFingerprint.DoesNotExist):
            profile.refresh_from_db()
