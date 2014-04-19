# coding=utf-8
from hashlib import sha1
import re

from django.conf import settings


class TransparentHashFactory(object):
    separator = '0gf'  # Make sure it validates to ".*[^0-9a-f].*", otherwise it may fail while decoding

    def get_used_prefix(self, prefix=None):
        if prefix:
            return prefix
        try:
            return getattr(self, 'transparent_hash_prefix')
        except AttributeError:
            pass
        try:
            return getattr(settings, "TRANSPARENT_HASH_PREFIX")
        except AttributeError:
            pass
        return None

    @staticmethod
    def hash_prefix_value(prefix: str, value) -> str:
        str_to_hash = "{prefix}{value}".format(prefix=prefix, value=value)
        str_to_hash = str_to_hash.encode('utf-8')
        return sha1(str_to_hash).hexdigest()

    def decode_from_thash(self, transparent_hash, prefix=None) -> str:
        if transparent_hash is None:
            raise ValueError  # TODO: give proper message to this exception

        used_prefix = self.get_used_prefix(prefix) or ''

        regex_res = re.match("(?P<inputed_hash>[0-9a-f]+)"+self.separator+"(?P<hex_value>[0-9a-f]+)",
                             transparent_hash)
        if regex_res is None:
            raise ValueError  # TODO: give proper message to this exception
        inputed_hash = regex_res.group('inputed_hash')
        hex_value = regex_res.group('hex_value')
        value = bytes.fromhex(hex_value).decode()
        the_hash = TransparentHashFactory.hash_prefix_value(used_prefix, value)

        if the_hash == inputed_hash:
            return value
        raise ValueError  # TODO: give proper message to this exception

    def encode_to_thash(self, value, prefix: str=None) -> str:
        if value is None:
            raise ValueError  # TODO: give proper message to this exception

        if isinstance(value, int):
            used_value = str(value)
        elif isinstance(value, str):
            used_value = value
        else:
            raise TypeError  # TODO: give proper message to this exception

        used_value_enc = used_value.encode()
        hex_value = "".join([format(c, 'x') for c in used_value_enc])

        used_prefix = self.get_used_prefix(prefix) or ''

        the_hash = TransparentHashFactory.hash_prefix_value(used_prefix, used_value)
        
        result = the_hash + self.separator + hex_value
        return result.lower()