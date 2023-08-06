__author__ = """Aria Bagheri"""
__email__ = 'ariab9342@gmail.com'
__version__ = '1.0.0'

from enum import Enum
from typing import List

import pyhibp
from pyhibp import pwnedpasswords

from walk_check import walk_checker

pyhibp.set_user_agent(ua="Python Password Security/1.0.0 (Library to check password security)")


class PasswordSecurityRequirement(Enum):
    USE_UPPERCASE = 1
    USE_LOWERCASE = 2
    USE_NUMBERS = 3
    USE_SPECIAL_CHARACTERS = 4
    AT_LEAST_16_CHARACTERS = 5
    NOT_PUBLICLY_KNOWN = 6
    NOT_KEYBOARD_WALK = 7


class PasswordSecurity:
    @staticmethod
    def verify_password(password: str, verifiers: List[PasswordSecurityRequirement] = None,
                        banned_words: list = None):
        if not verifiers:
            verifiers = [
                PasswordSecurityRequirement.USE_LOWERCASE,
                PasswordSecurityRequirement.USE_UPPERCASE,
                PasswordSecurityRequirement.USE_NUMBERS,
                PasswordSecurityRequirement.USE_SPECIAL_CHARACTERS,
                PasswordSecurityRequirement.AT_LEAST_16_CHARACTERS,
                PasswordSecurityRequirement.NOT_PUBLICLY_KNOWN,
                PasswordSecurityRequirement.NOT_KEYBOARD_WALK
            ]
        character_stats = PasswordSecurity.get_characters_stats(password)

        is_safe = True
        if banned_words:
            is_safe &= not any(map(lambda x: x in password, banned_words))
        if PasswordSecurityRequirement.AT_LEAST_16_CHARACTERS in verifiers:
            is_safe &= PasswordSecurity.is_password_long_enough(password)
        if is_safe and PasswordSecurityRequirement.USE_NUMBERS in verifiers:
            is_safe &= character_stats['has_numbers']
        if is_safe and PasswordSecurityRequirement.USE_LOWERCASE in verifiers:
            is_safe &= character_stats['has_lowercase']
        if is_safe and PasswordSecurityRequirement.USE_UPPERCASE in verifiers:
            is_safe &= character_stats['has_uppercase']
        if is_safe and PasswordSecurityRequirement.USE_UPPERCASE in verifiers:
            is_safe &= character_stats['has_special_characters']
        if is_safe and PasswordSecurityRequirement.NOT_PUBLICLY_KNOWN in verifiers:
            is_safe &= not PasswordSecurity.is_password_publicly_known(password)
        if is_safe and PasswordSecurityRequirement.NOT_KEYBOARD_WALK in verifiers:
            is_safe &= not PasswordSecurity.is_keyboard_walk(password)
        return is_safe

    @staticmethod
    def is_password_long_enough(password: str):
        return len(password) >= 16

    @staticmethod
    def get_characters_stats(password: str):
        has_uppercase = has_lowercase = has_numbers = has_special_characters = False
        for c in password:
            if not has_uppercase and c.isupper():
                has_uppercase = True
            if not has_lowercase and c.islower():
                has_lowercase = True
            if not has_numbers and c.isdigit():
                has_numbers = True
            if not has_special_characters and c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~":
                # https://owasp.org/www-community/password-special-characters
                has_special_characters = True
            if has_special_characters and has_numbers and has_uppercase and has_lowercase:
                break
        return {
            "has_numbers": has_numbers,
            "has_uppercase": has_uppercase,
            "has_lowercase": has_lowercase,
            "has_special_characters": has_special_characters,
        }

    @staticmethod
    def is_password_publicly_known(password: str):
        return pwnedpasswords.is_password_breached(password) != 0

    @staticmethod
    def is_keyboard_walk(password: str):
        return walk_checker(password, strict=False)
