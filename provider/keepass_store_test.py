import unittest
from keepass_store import KeepassStore


class TestBitwardenStore(unittest.TestCase):
    def test_get_and_cache_simple_entries(self):
        kps = KeepassStore('/Users/nick/PycharmProjects/password-lookup/provider/keepass.kdbx', True)
        entries = kps.get_and_cache_simple_entries()
        self.assertTrue(entries is not None)
        for entry in entries:
            print('items: {}'.format(entry))

if __name__ == "__main__":
    unittest.main()
