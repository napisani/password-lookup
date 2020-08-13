from simplecrypt import encrypt, decrypt
import os
import sys
import random
import string
import logging


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_key_filename(key_suffix):
    return (get_script_path() + "/{}.key").format(key_suffix)


def remove_key_file(key_suffix):
    if os.path.exists(get_key_filename(key_suffix)):
        os.remove(get_key_filename(key_suffix))


def get_key(key_suffix):
    try:
        with open(get_key_filename(key_suffix)) as key_file:
            return key_file.readline()
    except IOError:
        return generate_key(key_suffix)


def generate_key(key_suffix):
    logging.debug('generating key')
    key = get_random_string(256)
    with open(get_key_filename(key_suffix), "wb") as key_file:
        key_file.write(key)
    return key


class Session:
    session_file = '/tmp/{}.session'

    def __init__(self, key_suffix, session_suffix):
        self.key_suffix = key_suffix
        self.session_suffix = session_suffix
        self.session = None

    def _remove_session_file(self):
        if os.path.exists(self.get_session_file()):
            os.remove(self.get_session_file())

    def clear(self):
        self.session = None
        remove_key_file(self.key_suffix)
        self._remove_session_file()

    def load(self):
        self.session = self.read()

    def get_session_file(self):
        return Session.session_file.format(self.session_suffix)

    def set(self, session):
        self.session = session

    def write(self):
        with open(self.get_session_file(), "w") as f:
            key = get_key(self.key_suffix)
            f.write(encrypt(key, self.session.encode()))

    def read(self):
        try:
            with open(self.get_session_file()) as f:
                key = get_key(self.key_suffix)
                logging.debug('decrypting with key ' + key)
                self.session = decrypt(key, f.readline()).decode()
                # Do something with the file
        except IOError:
            logging.debug("read File not accessible")
            self.session = ''
        return self.session
