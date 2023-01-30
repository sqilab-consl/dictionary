# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import hashlib
import binascii
from passlib.hash import pbkdf2_sha256
# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/
PASSWORD_ITERATIONS=100000
SALT_SIZE=60
PASSWORD_ALGORITHM='sha512'


def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(SALT_SIZE)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(PASSWORD_ALGORITHM, password.encode('utf-8'),
                                  salt, PASSWORD_ITERATIONS)
    pwdhash = binascii.hexlify(pwdhash)
    salt_b64=binascii.b2a_base64(salt,newline=False).decode()
    pwd_b64=binascii.b2a_base64(pwdhash,newline=False).decode()
    return "{}${}${}${}".format(PASSWORD_ALGORITHM,PASSWORD_ITERATIONS, salt_b64, pwd_b64)  # return bytes


def verify_pass(provided_password, stored_password:str):
    """Verify a stored password against one provided by user"""
    hash_parts = stored_password.split('$')
    if len(hash_parts)!=4:
        return False
    stored_password = binascii.a2b_base64(hash_parts[3])
    stored_salt=binascii.a2b_base64(hash_parts[2])
    pwdhash = hashlib.pbkdf2_hmac(hash_parts[0],
                                  provided_password.encode('utf-8'),
                                  stored_salt,
                                  int(hash_parts[1]))
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    print("Original: {}\nNEW: {}".format(stored_password.decode(),pwdhash))
    return pwdhash == stored_password.decode()
