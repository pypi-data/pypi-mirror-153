from unittest import TestCase

from openmodule.utils.charset import Charset, CharsetConverter, legacy_lpr_charset


class CharsetModelTest(TestCase):
    def test_uppercase_on_construct(self):
        charset = Charset(allowed="abc")
        self.assertEqual("ABC", charset.allowed)

    def test_uppercase_on_assign(self):
        charset = Charset(allowed="")
        self.assertEqual("", charset.allowed)

        charset.allowed = "abc"
        self.assertEqual("ABC", charset.allowed)

    def test_replacements(self):
        charset = Charset(allowed="abc", replacements=[{"from": "x", "to": "a"}])
        cleaned = CharsetConverter(charset).clean(" abcx ")
        self.assertEqual("ABCA", cleaned)

    def test_replacement_to_non_allowed(self):
        charset = Charset(allowed="abc", replacements=[{"from": "x", "to": "y"}])
        cleaned = CharsetConverter(charset).clean(" abcx ")
        self.assertEqual("ABC", cleaned)

    def test_legacy_charset(self):
        cc = CharsetConverter(legacy_lpr_charset)
        clean = cc.clean("abcdefghijklmnopqrstuvwxyz1234567890üäö-_'*:;")
        self.assertEqual("ABCDEFGHIJKLMN0P0RSTUVWXYZ1234567890UA0", clean)
