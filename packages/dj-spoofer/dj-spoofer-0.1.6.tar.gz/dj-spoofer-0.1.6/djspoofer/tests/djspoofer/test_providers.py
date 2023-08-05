from django.test import TestCase

from djspoofer import providers
from djspoofer.providers import UsernameProvider


class UsernameProviderTests(TestCase):
    """
    Username Provider Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.username = 'username_123'
        cls.test_str = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

    def test_generate_digits(self):
        val = providers.generate_digits(n_digits=14)
        self.assertTrue(len(str(val)) == 14)

        val = providers.generate_digits(n_digits=99)
        self.assertTrue(len(str(val)) == 99)

    def test_replace_character(self):
        val = providers.replace_character(self.test_str, 15, char='X')
        self.assertEquals(val, 'Lorem ipsum dolXr sit amet, consectetur adipiscing elit.')

    def test_reverse(self):
        self.assertEquals(UsernameProvider.reverse(self.username), '321_emanresu')

    def test_repeat(self):
        self.assertEquals(UsernameProvider.repeat(self.username, chance=0), 'username_123')
        self.assertEquals(UsernameProvider.repeat(self.username, chance=1), 'uusseerrnnaammee__112233')

    def test_replace(self):
        self.assertEquals(UsernameProvider.replace(self.username, chance=0), 'username_123')
        self.assertNotEquals(UsernameProvider.replace(self.username, chance=1), 'username_123')

    def test_concat(self):
        word_2 = 'hello'
        new_username = UsernameProvider.concat(self.username, word_2, chance=1)
        self.assertTrue(new_username.startswith(self.username.capitalize()))
        self.assertTrue(new_username.endswith('Hello'))

        word_2 = 'hello'
        new_username = UsernameProvider.concat(self.username, word_2, chance=0)
        self.assertTrue(new_username.startswith(self.username))
        self.assertTrue(new_username.endswith('hello'))

    def test_vowel_remove(self):
        new_username = UsernameProvider.vowel_remove(self.username, chance=0)
        self.assertEquals(new_username, self.username)

        new_username = UsernameProvider.vowel_remove(self.username, chance=1)
        self.assertEquals(new_username, 'srnm_123')

    def test_concat_digits(self):
        new_username = UsernameProvider.concat_digits(self.username, chance=1)
        self.assertIn(len(new_username), [13, 14])

    def test_decorate(self):
        new_username = UsernameProvider.decorate(self.username, chance=0, min_chars=0, max_chars=0)
        self.assertEquals(new_username, self.username)

        new_username = UsernameProvider.decorate(self.username, chance=1, min_chars=3, max_chars=3)
        self.assertEquals(len(new_username), 18)

    def test_leet(self):
        new_username = UsernameProvider.leet(self.username, chance=0)
        self.assertEquals(new_username, self.username)

        new_username = UsernameProvider.leet(self.username, chance=1)
        self.assertEquals(new_username, 'u53rn4m3_123')

    def test_honorific(self):
        new_username = UsernameProvider.honorific(self.username, chance=0)
        self.assertFalse(new_username[0].isupper())

        new_username = UsernameProvider.honorific(self.username, chance=1)
        self.assertTrue(new_username[0].isupper())
