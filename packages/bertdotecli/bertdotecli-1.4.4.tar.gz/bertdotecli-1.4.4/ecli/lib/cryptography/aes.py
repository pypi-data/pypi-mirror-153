from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import argparse
import io
import json
import os
import base64
import sys

# Cryptography modules
try:
    from Crypto import Random
    from Crypto.Cipher import AES
except ImportError:
    raise ImportError(
        "Cryptographic Library not detected!\n"\
        "Install with `pip install pycryptodome`"
    )

# Cryptography init
default_encryption_mode = AES.MODE_ECB
valid_key_lengths = [16, 24, 32]

class DecryptionError(Exception):
    pass

class EncryptionError(Exception):
    pass

class ParseError(Exception):
    pass

class FSOError(Exception):
    pass

class AESCipher:

    def __init__(self, **kwargs):

        self.bs = AES.block_size
        self.mode = kwargs['mode'] if kwargs.get('mode') else default_encryption_mode
        self.key_length = 0
        self.key = None

    def HandleErr(self, exception, message):
        if sys.version_info[0] >= 3:
            quit(message)
        else:
            raise exception(message)

    def ReadKey(self, keyinput, read_mode='utf-8'):

        if os.path.isfile(os.path.expanduser(keyinput)):
            keyinput = os.path.expanduser(keyinput)
            if os.path.exists(keyinput):
                if read_mode == 'bytes':
                    key = open(keyinput, 'rb').read()
                    self.key_length = len(key)
                else:
                    try:
                        with io.open(keyinput,"r", encoding="utf-8") as fileobj:
                            key = fileobj.read()
                            self.key_length = len(key)
                            if(self.key_length not in valid_key_lengths):
                                self.HandleErr(ParseError, "{k} key must be either 16, 24, or 32 characters long, but got {d}".format(
                                    k=keyinput, d=len(key)))
                            else:
                                try:
                                    key=key.encode()
                                except Exception as err:
                                    HandleErr(ParseError,"Failed to encode the input key '{k}', error was {e}.".format(k=keyinput, e=err))
                    except Exception as err:
                        self.HandleErr(FSOError, 'Failed to read the specified key file, error was %s' % err)
            else:
                self.HandleErr(FSOError, 'The key file you specified (%s) does not exist' % key)
        else:
            try:
                key = base64.b64decode(keyinput)
                self.key_length = len(key)
            except Exception as err:
                self.HandleErr(ParseError, "Failed to decode the input key string '{k}'. Error was {e}.".format(k=keyinput, e=err))
        self.key = key

    def encrypt(self, message, verbosity=0):
        pad_len = self.key_length - len(message) % self.key_length
        padding = chr(pad_len) * pad_len
        message += padding
        iv = Random.new().read(self.bs)
        if self.mode == AES.MODE_CBC:
            cryptor = AES.new(self.key, self.mode, iv)
        else:
            # We don't need an initialization vector for ECB mode of operation
            if verbosity >= 3:
                print('Skipped initialization vector (IV), as ECB mode was detected')
            cryptor = AES.new(self.key, self.mode)
        try:
            if sys.version_info[0] >= 3:
                data = cryptor.encrypt(message.encode('utf-8'))
            else:
                data = cryptor.encrypt(message)
        except Exception as err:
            self.HandleErr(EncryptionError, "Failed to encrypt the input string {m} using the key specified {k}, error was {e}".format(
                m=message, 
                k=self.key,
                e=err
                ))
        return base64.b64encode(data).decode('utf-8')

    def decrypt(self, message):
        message = base64.b64decode(message.encode('utf-8'))
        if self.mode == AES.MODE_CBC:
            iv = message[:AES.block_size]
            cryptor = AES.new(self.key, self.mode, iv)
        else:
            cryptor = AES.new(self.key, self.mode)
        try:
            c_text = cryptor.decrypt(message)
            # Apply PKCS#5/PKCS#7 padding
            pad_len = ord(c_text.decode('utf-8')[-1])
            clear_text = c_text.decode('utf-8')[:-pad_len]
        except Exception as err:
            self.HandleErr(DecryptionError, "Failed to decrypt the input string {m} using the key specified {k}".format(m=message, k=self.key))
        return clear_text