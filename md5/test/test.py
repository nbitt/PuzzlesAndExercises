import unittest
from md5 import md5
from bitarray import bitarray

class TestMd5(unittest.TestCase):

    def test_blank(self):
        test = md5.Md5("")
        digest = test.digest()
        self.assertEqual('d41d8cd98f00b204e9800998ecf8427e', digest)

    def test_load_file (self):
        file = "blank.txt"
        self.assertEqual(bitarray('0'), md5.Md5(file).load_message(file))

    def test_padding (self):
        file = "blank.txt"
        test = md5.Md5(file)
        msg_bitarray = test.perform_padding(self, self.msg_bitarray)  # update bitarray
        correct_bitstring = '10000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
                            '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
                            '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
                            '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
                            '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
                            '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        correct = bitarray(endian='little')
        for bit in correct_bitstring:
            correct.append(int(bit))

        self.assertEqual(correct, msg_bitarray)  # little endian

    def test_modular_add (self):
        # Note: all values are little endian
        test = md5.Md5("")

        # Test values (bitarrays are expected input type)
        bitarray_1 = bitarray('100', endian='little')
        bitarray_2 = bitarray('010', endian='little')
        bitarray_7 = bitarray('111', endian='little')
        bitarray_0 = bitarray('000', endian='little')

        self.assertEqual(bitarray_2, test.modular_add(bitarray_1, bitarray_1, 2**3, 3))
        self.assertEqual(bitarray_0, test.modular_add(bitarray_1, bitarray_7, 2**3, 3))
        self.assertEqual(bitarray_1, test.modular_add(bitarray_2, bitarray_7, 2 ** 3, 3))

    def test_circular_leftshift (self):
        test = md5.Md5("")

        # Note: expects 32-bit values
        bitarray_in = bitarray('11000000000000000000000000000000', endian='little')
        bitarray_ou = bitarray('10000000000000000000000000000001', endian='little')
        self.assertEqual(bitarray_ou, test.circular_leftrotate(bitarray_in, shift_cnt=1))

        bitarray_ou = bitarray('00000000000000000000000000000011', endian='little')
        self.assertEqual(bitarray_ou, test.circular_leftrotate(bitarray_in, shift_cnt=2))


if __name__ == '__main__':
    unittest.main()