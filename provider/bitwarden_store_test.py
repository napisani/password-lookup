import unittest
from bitwarden_store import BitwardenStore


class TestBitwardenStore(unittest.TestCase):

    def test_get_and_cache_simple_entries(self):
        bw = BitwardenStore(True)
        entries = bw.get_and_cache_simple_entries()
        self.assertTrue(entries is not None)
        for entry in entries:
            print('items: {}'.format(entry))


if __name__ == "__main__":
    unittest.main()
