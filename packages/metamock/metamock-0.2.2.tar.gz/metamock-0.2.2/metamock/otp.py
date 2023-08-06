import base64
import hashlib
import hmac
import time
from datetime import datetime


class Totp(object):
    def __init__(
        self, secret, interval_secs=30, digits=6, digest=hashlib.sha1
    ):
        """
        Create a new TOTP code generator.

        Parameters:
         secret (string|list of byte): shared secret as either a base32 encoded string or byte array
         interval_secs (int): interval, in seconds, to generate codes at
         digits (int): number of digits in the generated codes
         digest (function): HMAC digest function to use
        """
        if isinstance(secret, str):
            secret = secret_to_bytes(secret)

        self.secret = secret
        self.interval_secs = interval_secs
        self.digits = digits
        self.digest = digest

    def generate(self, at=None):
        """
        Generate a new OTP code.

        Parameters:
         at (datetime): timestamp to generate the code for or None to use current time

        Returns:
         (int): generated code
        """
        timecode = self.__timecode(at or datetime.now())
        hmac_hash = hmac.new(self.secret, timecode, self.digest).digest()

        offset = ord(hmac_hash[19]) & 0xF
        code = (
            (ord(hmac_hash[offset]) & 0x7F) << 24
            | (ord(hmac_hash[offset + 1]) & 0xFF) << 16
            | (ord(hmac_hash[offset + 2]) & 0xFF) << 8
            | (ord(hmac_hash[offset + 3]) & 0xFF)
        )

        return code % 10**self.digits

    def __timecode(self, at):
        return timestamp_to_bytestring(
            int(time.mktime(at.timetuple()) / self.interval_secs)
        )


def secret_to_bytes(secret):
    """Convert base32 encoded secret string to bytes"""
    return base64.b32decode(secret)


def timestamp_to_bytestring(val, padding=8):
    """Convert Unix timestamp to bytes"""
    result = []

    while val != 0:
        result.append(chr(val & 0xFF))
        val = val >> 8

    return "".join(reversed(result)).rjust(padding, "\0")
