# =====================
# IMPORTS
# =====================
import argparse
import os
from bitarray import bitarray
from math import floor, sin

class Md5:
    """ RSA Data Security, Inc. MD5 Message-Digest Algorithm
        Based on reading from: https://en.wikipedia.org/wiki/MD5

        From Wikipedia:
        > Input message is padded, then chopped up into blocks of 512 bits.
        > the MD5 alg operates on a 128-bit state (which becomes final digest)
        The 128-bit state is divided into 4, 32-bit pieces ("words"): called
        A, B, C, D -- each of these words is initialzed with fixed constants.

    """
    def __init__(self, input):
        self.msg_bitarray = self.load_message(input)
        self.output_hash = ""  # init empty string

        # "K[i] denotes a 32-bit constant, different for each (of 64) operation" - wiki
        # Binary integer part of the sines of integers (units radians) as constants:
        self.K = []  # init empty list
        for i in range(0, 64):
            val = floor(abs(sin(i + 1)) * 2**32)
            self.K.append(hex(val))

        self.A = 0x67452301 # "A" (see notes)
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476

    def load_message (self, input):
        """ Takes file or string as input"""

        if os.path.isfile(input):
            with open(input, "rb") as f:  # read binary
                msg = f.read()
        else:
            # Must convert string to binary:
            msg = bytes(input, 'utf-8')

        # Bytes are converted to binary format and appended to bitarray
        binary = "0" + '0'.join(format(x, 'b') for x in msg)  # standard chars start with 0

        return bitarray(binary)  # return bitarray

    def perform_padding (self):
        """ Perform required padding to message """

        # Record length
        msg_len = len(self.msg_bitarray)

        # First add a single "1" bit to message:
        self.msg_bitarray.append(1)

        # append "0" bit until msg len in bits ≡ 448 (mod 512)
        while (len(self.msg_bitarray) % 512) != 448:
            self.msg_bitarray.append(0)

        # Append original length in bits mod 2**64 to msg
        print("TODO")

        print(self.msg_bitarray)

    def digest (self):
        self.perform_padding()


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
