""" RSA Data Security, Inc. MD5 Message-Digest Algorithm
    Based on reading from: https://en.wikipedia.org/wiki/MD5

    From Wikipedia:
    > Input message is padded, then chopped up into blocks of 512 bits.
    > the MD5 alg operates on a 128-bit state (which becomes final digest)
    The 128-bit state is divided into 4, 32-bit pieces ("words"): called
    A, B, C, D -- each of these words is initialzed with fixed constants.
    > "All values are in little-endian"

    ALSO USEFUL:
    https://www.rfc-editor.org/rfc/rfc1321

    TODO:
     1. learn more about class vs static methods and update.
     https://www.geeksforgeeks.org/class-method-vs-static-method-python/

"""

# =====================
# IMPORTS
# =====================
import argparse
import os
from bitarray import bitarray
from math import floor, sin

# =====================
# CLASS DEF
# =====================

class Md5:

    def __init__(self, input):
        self.msg_bitarray = self.load_message(input)
        self.output_hash = ""  # init empty string

        # "K[i] denotes a 32-bit constant, different for each (of 64) operation" - wiki
        # Binary integer part of the sines of integers (units radians) as constants:
        self.K_SINES = []  # init empty list. denoted "K" in refs
        for i in range(0, 64):
            val = floor(abs(sin(i + 1)) * 2**32)
            self.K_SINES.append(bitarray(self.num_to_lendian_bitstr(val, 32), endian='little'))

        # "Each round has a repeated seq. of 4 shift amounts... execute over 16-word block"
        # Init constant shift amounts (optimized empirically, see md5 specification)
        self.SHIFTS = [
            [7, 12, 17, 22],  # round 1
            [5, 9, 14, 20],  # round 2
            [4, 11, 16, 23],  # etc...
            [6, 10, 15, 21],
        ]  # denoted "S" in spec/refs

        # Init 32-bit "words" that alg operates on/modifies. "A":"D" (see notes)
        self.a0 = bitarray(self.num_to_lendian_bitstr(0x67452301, 32), endian='little')
        self.b0 = bitarray(self.num_to_lendian_bitstr(0xefcdab89, 32), endian='little')
        self.c0 = bitarray(self.num_to_lendian_bitstr(0x98badcfe, 32), endian='little')
        self.d0 = bitarray(self.num_to_lendian_bitstr(0x10325476, 32), endian='little')

    def perform_padding (self):
        """ Perform required padding to message """

        # Record length
        msg_len = len(self.msg_bitarray)

        # First add a single "1" bit to message:
        self.msg_bitarray.append(1)

        # append "0" bit until msg len in bits ≡ 448 (mod 512)
        while (len(self.msg_bitarray) % 512) != 448:
            self.msg_bitarray.append(0)

        # Append original length in bits (mod 2**64) to msg
        for bit in self.num_to_lendian_bitstr(msg_len % 2**64, 64):
            self.msg_bitarray.append(int(bit))

    def digest (self):
        """ Execute main md5 alg. Operates on 128-bit word to make final hash (digest)"""
        # First perform required padding (multiple of 512):
        self.perform_padding()  # updates self.msg_bitarray

        # Process the message in successive 512-bit chunks:
        for blk_offset in range(0, int(len(self.msg_bitarray)), 512): # step 512
            # Get current block of 512-bits:
            blk_512_bits = self.msg_bitarray[blk_offset: blk_offset + 512]

            # Now break 512-bit block into sixteen 32-bit words M[j], 0 ≤ j ≤ 15
            m_32bit_words = []  # (re-)init empty. "M" in references
            for i in range(0, 512, 32):
                m_32bit_words.append(blk_512_bits[i: i+16])

            # Init hash values (128-bit broken up into 4 chunks) for block:
            a_hash = self.a0  # denoted "A" in spec
            b_hash = self.b0  # denoted "B" in spec
            c_hash = self.c0  # etc...
            d_hash = self.d0

            # "Main Loop" -- execute operations
            # Note to self: "^" is bitwise XOR, "|" is bitwise OR, "&" is bitwise AND, "~" is NOT
            for i in range(0, 64):
                # NOTE: "fcn" is one of 4 possible nonlinear functions
                # "fcn" is denoted "F" in specs/references
                # TODO: read spec on where "g" comes from

                # Round 1 nonlinear fcn
                if 0 <= i <= 15:
                    fcn = (b_hash & c_hash) | ((~b_hash) & d_hash)
                    g = i
                    shifts = self.SHIFTS[0]  # repeated seq. of shift amts for round
                # Round 2 nonlinear fcn
                elif 16 <= i <= 31:
                    fcn = (b_hash & d_hash) | (c_hash & (~d_hash))
                    g = (5*i + 1) % 16
                    shifts = self.SHIFTS[1]  # repeated seq. of shift amts for round

                # Round 3 nonlinear fcn
                elif 32 <= i <= 47:
                    fcn = b_hash ^ c_hash ^ d_hash
                    g = (3*i + 5) % 16
                    shifts = self.SHIFTS[2]  # repeated seq. of shift amts for round

                elif 48 <= i <= 63:
                    fcn = c_hash ^ (b_hash | (~d_hash))
                    g = (7*i) % 16
                    shifts = self.SHIFTS[3]  # repeated seq. of shift amts for round
                # end if

            # Note: modular addition is used in md5 alg
            fcn = self.modular_add(fcn, a_hash, modulus=2**32, bits=32)
            fcn = self.modular_add(fcn, self.K_SINES[i], modulus=2**32, bits=32)
            fcn = self.modular_add(fcn, m_32bit_words[g], modulus=2 ** 32, bits=32)
            fcn = self.circular_leftrotate(fcn, shifts[i % 4])  # mod four to repeat shift pattern

            # "Jumble" the 32-bit words of the hash "A, B, C, D"
            a_hash = d_hash
            d_hash = c_hash
            c_hash = b_hash
            b_hash = self.modular_add(b_hash, fcn)

            # end i in range(0, 64):

            # Add this chunk's hash to result so far:
            self.a0 = a_hash
            self.b0 = b_hash
            self.c0 = c_hash
            self.d0 = d_hash

        # end for blk_offset in range(...)

        digest = self.a0 + self.b0 + self.c0 + self.d0
        print(self.bin_to_hex(digest))  # confirmed hex convert working correctly

    @staticmethod
    def load_message (input):
        """ Takes file or string as input - note that utf-8 chars are big endian"""

        if os.path.isfile(input):
            with open(input, "rb") as f:  # read binary
                msg = f.read()
        else:
            # Must convert string to binary:
            msg = bytes(input, 'utf-8')

        # Bytes are converted to binary format and appended to bitarray
        binary = "0" + '0'.join(format(x, 'b') for x in msg)  # standard chars start with 0

        # return bitarray - convert to little endian
        return bitarray(binary, endian='little')

    @staticmethod
    def num_to_lendian_bitstr(integer, bits):
        tmp = "{0:b}".format(integer)[::-1]  # binary format into "{}" placeholder, reversed for little endian
        if len(tmp) > bits:
            print(f"ERROR: {integer} causes integer overflow for size {bits}")
        while len(tmp) < bits:
            tmp += '0'  # trailing zeros, as needed
        return tmp

    @staticmethod
    def modular_add (bitarray_1, bitarray_2, modulus=2**32, bits=32):
        val_1 = int.from_bytes(bitarray_1.tobytes(), 'little')  # little endian conversion to value
        val_2 = int.from_bytes(bitarray_2.tobytes(), 'little')# little endian conversion to value

        ans = (val_1 + val_2) % modulus  # execute modular arithmetic

        tmp = "{0:b}".format(ans)[::-1]  # binary format into "{}" placeholder, reversed for little endian
        if len(tmp) > bits:
            print(f"ERROR: modular arithmatic integer overflow for size {bits}")
        while len(tmp) < bits:
            tmp += '0'  # trailing zeros, as needed
        return bitarray(tmp, endian='little')

    @staticmethod
    def circular_leftrotate (bit_array, shift_cnt):
        """ Notes from Wiki page:
        > Leftrotate function definition: (x << c) binary OR (x >> (32-c))
        (where c is shift amount)
        > The "<<" bitwise operator shifts bits to the left. Excess bits
        shifted off to the left are discarded. Zeros inserted from right.

        This function shifts left by shift_cnt, inserting zeros while also
        shifting right by 32 (len of bitarray) minus shift. Logical OR
        then combines two shifts to produce "circular" shift.
        """
        return (bit_array << shift_cnt) | (bit_array >> (32 - shift_cnt))

    @staticmethod
    def bin_to_hex (digest):
        """ Convert 128-bit binary digest to hex"""
        HEX_MAP = {
            '0000': "0",
            '0001': "1",
            '0010': "2",
            '0011': "3",
            '0100': "4",
            '0101': "5",
            '0110': "6",
            '0111': "7",
            '1000': "8",
            '1001': "9",
            '1010': "a",
            '1011': "b",
            '1100': "c",
            '1101': "d",
            '1110': "e",
            '1111': "f",
        }
        digest = digest.tolist()  # convert bit array to list

        # Break into 4-bit chunks for hex values
        hex_hash = ''
        for i in range(0, 128, 4):
            hex_hash += HEX_MAP[''.join(str(x) for x in digest[i:(i+4)])]

        return hex_hash

# =====================
# HELPER
# =====================

def handle_arguments ():
    """ """
    parser = argparse.ArgumentParser(
        description="Generates m5d hash for a string or file. Only supports standard 8-bit characters",
        usage="python %(prog)s <string | filepath>"
    )

    parser.add_argument('input', nargs="+", type=str)  # required

    args = parser.parse_args()

    return args.input[0]


# =====================
# MAIN
# =====================


def main ():
    md5 = Md5(handle_arguments())
    md5.digest()

# =====================
# ENTRY POINT
# =====================


if __name__ == '__main__':
    main()
