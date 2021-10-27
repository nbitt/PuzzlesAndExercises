import unittest
from md5 import md5

class TestMd5(unittest.TestCase):

    def test_blank(self):
        test = md5.Md5("")
        digest = test.digest()
        self.assertEqual('d41d8cd98f00b204e9800998ecf8427e', digest)

if __name__ == '__main__':
    unittest.main()