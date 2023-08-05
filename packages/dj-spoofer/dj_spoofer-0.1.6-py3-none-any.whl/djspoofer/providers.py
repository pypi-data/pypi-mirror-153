import logging
import random
import string

from faker.providers import BaseProvider

from djstarter import utils
from . import dictionary

logger = logging.getLogger(__name__)


class UsernameProvider(BaseProvider):
    """
        Provider to generate human-looking usernames

        from faker import Faker
        from .providers import UsernameProvider
        fake = Faker()
        fake.add_provider(UsernameProvider)
        username = fake.username()
    """

    __provider__ = 'username'
    __lang__ = 'en_US'

    words = []
    MIN_LEN = 5
    MAX_LEN = 20
    VOWELS = 'aeiou'
    SEPARATORS = ('_', '-', 'x', 'X', 'o', 'O', '0', '1')
    CONJUNCTIONS = ('-and-', '_and_', '-or-', '_or_', '-with-', '_with_', '-nor-', '_nor_', '-for-', '_for_')
    HONORIFICS = ('Mr', 'Mister', 'Ms', 'Miss', 'Mrs', 'Master', 'Sir', 'Madam', 'Dame', 'Lord', 'Lady', 'Dr',
                  'Prof', 'Sr', 'Fr', 'Rev', 'Elder', 'Judge', 'Duke')

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):   # pragma: no cover
            cls.words = cls.load_words()
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def rand_word(self):
        return random.choice(self.words)

    def username(self):
        word = self.rand_word
        alg_map = {
            self.repeat: (word,),
            self.replace: (word,),
            self.concat: (word, self.rand_word),
            self.vowel_remove: (word,),
            self.concat_digits: (word,),
            self.decorate: (word,),
            self.leet: (word,),
            self.honorific: (word,),
        }
        alg = random.choice(list(alg_map.keys()))
        args = alg_map[alg]
        new_word = alg(*args)[:self.MAX_LEN]
        return self.reverse(word) if new_word == word else new_word

    @classmethod
    def load_words(cls):
        return [word.strip() for word in dictionary.ENGLISH_WORDS if (cls.MIN_LEN <= len(word) <= cls.MAX_LEN)]

    @classmethod
    def reverse(cls, word):
        return word[::-1]

    @classmethod
    def repeat(cls, word, chance=.1):
        return ''.join(i + i if utils.dice_roll(chance) else i for i in word)

    @classmethod
    def replace(cls, word, chance=.1):
        new_letters = []
        for i, letter in enumerate(word):
            if utils.dice_roll(chance):
                new_letters.append(random.choice(string.ascii_lowercase.replace(letter, '')))
            else:
                new_letters.append(letter)
        return ''.join(new_letters)

    @classmethod
    def concat(cls, word1, word2, chance=.3):
        word1 = word1.capitalize() if utils.dice_roll(chance) else word1
        word2 = word2.capitalize() if utils.dice_roll(chance) else word2
        space = random.choice(cls.SEPARATORS+cls.CONJUNCTIONS)
        return f'{word1}{space}{word2}'

    @classmethod
    def vowel_remove(cls, word, chance=.1):
        return ''.join('' if utils.dice_roll(chance) and i in cls.VOWELS else i for i in word)

    @classmethod
    def concat_digits(cls, word, chance=.5):
        digits = str(generate_digits(random.randint(1, 2)))
        return word + digits if utils.dice_roll(chance) else digits + word

    @classmethod
    def decorate(cls, word, chance=.5, min_chars=1, max_chars=3):
        l_deco = ''.join(random.choice(cls.SEPARATORS) for _ in range(random.randint(min_chars, max_chars)))
        r_deco = l_deco[::-1] if utils.dice_roll(chance) else ''  # Slicing syntax means reverse string
        return f'{l_deco}{word}{r_deco}'

    @classmethod
    def leet(cls, text, chance=.33):
        leet_map = {
            'o': '0',
            'i': '1',
            'e': '3',
            'a': '4',
            's': '5',
            't': '7',
        }

        for symbol, replaceStr in leet_map.items():
            if utils.dice_roll(chance):
                text = text.replace(symbol, replaceStr)
                text = text.replace(symbol.upper(), replaceStr)
        return text

    @classmethod
    def honorific(cls, word, chance=.5):
        h = random.choice(cls.HONORIFICS)
        h = h.title() if utils.dice_roll(chance) else h.lower()
        return f'{h}{random.choice(cls.SEPARATORS)}{word}'


class PhoneNumberProvider(BaseProvider):
    """
        Provider to generate human-looking usernames

        from faker import Faker
        from .providers import UsernameProvider
        fake = Faker()
        fake.add_provider(PhoneNumberProvider)
        username = fake.username()
    """

    __provider__ = 'phone_number'
    __lang__ = 'en_US'

    @classmethod
    def us_e164(cls):
        return f'+1{generate_digits(10)}'


def generate_digits(n_digits):
    return random.randint(10 ** (n_digits - 1), (10 ** n_digits) - 1)


def replace_character(orig_str, idx, char):
    return orig_str[:idx] + char + orig_str[idx + 1:]
