import unittest
from .session import Session


class SessionTest(unittest.TestCase):

    def test(self):
        s = Session('unit_test', 'unit_test')
        s.clear()
        s.load()
        print(s.read())
        s.write()
        s.read()


if __name__ == "__main__":
    unittest.main()
