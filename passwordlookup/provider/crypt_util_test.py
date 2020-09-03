import unittest
from .crypt_util import CryptUtil


class CryptUtilTest(unittest.TestCase):

    def test(self):
        cu = CryptUtil()
        key = cu.generate_key()
        print(key)
        cu.write_key_to_file('/Users/nick/PycharmProjects/password-lookup/provider/cu_test.key', key)
        key2 = cu.read_key_from_file('/Users/nick/PycharmProjects/password-lookup/provider/cu_test.key')
        self.assertTrue(key2 == key)

        msg = 'test message'
        enc_msg = cu.encrypt_str(msg, key)
        dec_msg = cu.decrypt_bytes(enc_msg, key)
        print(msg)
        print(dec_msg)
        self.assertTrue(dec_msg == msg)


if __name__ == "__main__":
    unittest.main()
