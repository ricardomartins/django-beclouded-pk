import re

from django.test import TestCase

from .transparent_hashs import TransparentHashFactory


class TransparentHashFactoryTests(TestCase):
    def test_encode_decode_valid_string_no_prefix(self):
        obj = TransparentHashFactory()

        initial_pk = "10"

        hsh = obj.encode_to_thash(initial_pk)
        final_pk = obj.decode_from_thash(hsh)

        self.assertEqual(int(initial_pk), int(final_pk))

    def test_encode_decode_valid_int_no_prefix(self):
        obj = TransparentHashFactory()

        initial_pk = 10

        hsh = obj.encode_to_thash(initial_pk)
        final_pk = obj.decode_from_thash(hsh)

        self.assertEqual(int(initial_pk), int(final_pk))

    def test_encode_decode_valid_string_with_prefix(self):
        obj = TransparentHashFactory()

        initial_pk = "10"

        hsh = obj.encode_to_thash(initial_pk, 'prefix')
        final_pk = obj.decode_from_thash(hsh, 'prefix')

        self.assertEqual(int(initial_pk), int(final_pk))

    def test_encode_decode_valid_int_with_prefix(self):
        obj = TransparentHashFactory()

        initial_pk = 10

        hsh = obj.encode_to_thash(initial_pk, 'prefix')
        final_pk = obj.decode_from_thash(hsh, 'prefix')

        self.assertEqual(int(initial_pk), int(final_pk))

    def test_encode_none(self):
        obj = TransparentHashFactory()

        initial_pk = None

        try:
            obj.encode_to_thash(initial_pk)
        except ValueError:
            pass
        else:
            self.assertEqual(True, False, "Pk passed to encode_pk is None, it should raise a ValueError")

    def test_decode_none(self):
        obj = TransparentHashFactory()

        hsh = None

        try:
            obj.decode_from_thash(hsh)
        except ValueError:
            pass
        else:
            self.assertEqual(True, False, 'None passed to decode_pk, it should raise a ValueError.')

    def test_decode_wrong_hash(self):
        obj = TransparentHashFactory()

        initial_pk = 10

        hsh = obj.encode_to_thash(initial_pk)
        hsh = "b" + hsh

        try:
            obj.decode_from_thash(hsh)
        except ValueError:
            pass
        else:
            self.assertEqual(True, False, 'Hash passed to decode_pk is wrong, it should raise a ValueError.')

    def test_decode_wrong_value(self):
        obj = TransparentHashFactory()

        initial_pk = 10

        hsh = obj.encode_to_thash(initial_pk)
        regex_res = re.match("(?P<inputed_hash>[0-9a-f]+)"+obj.separator+"(?P<hex_value>[0-9a-f]+)",
                             hsh)
        inputed_hash = regex_res.group('inputed_hash')
        hex_value = regex_res.group('hex_value')
        hex_value += "a"
        hsh = "".join([inputed_hash, obj.separator, hex_value])

        try:
            obj.decode_from_thash(hsh)
        except ValueError:
            pass
        else:
            self.assertEqual(True, False, 'Pk passed to decode_pk is wrong, it should raise a ValueError.')

    def test_decode_missing_breaks(self):
        obj = TransparentHashFactory()

        initial_pk = 10

        hsh = obj.encode_to_thash(initial_pk)
        regex_res = re.match("(?P<inputed_hash>[0-9a-f]+)"+obj.separator+"(?P<hex_value>[0-9a-f]+)",
                             hsh)
        inputed_hash = regex_res.group('inputed_hash')
        hex_value = regex_res.group('hex_value')

        hsh = "".join([inputed_hash, hex_value])

        try:
            obj.decode_from_thash(hsh)
        except ValueError:
            pass
        else:
            self.assertEqual(True, False, 'String passed to decode_pk is badly formed, it should raise a ValueError.')
