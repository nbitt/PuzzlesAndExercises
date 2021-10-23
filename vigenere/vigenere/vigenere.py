# =====================
# IMPORTS
# =====================
import argparse
import sys

# =====================
# Classes
# =====================
import string


class EncoderDecoder:
    def __init__(self, direction, msg, key):
        if direction == "encode":
            self.direction = 1
        else:
            self.direction = -1
        self.msg = msg.lower().replace(" ", "")  # no spaces allowed for more secure encoding
        self.key = key.lower()
        self.ALPHABET = list(string.ascii_lowercase)  # used for encoding/decoding
        self.output = ""  # init empty for output

    def process (self):

        # Define "rotation" array for key - Note: all rots are pos./fwd rotations
        self.key_rots = []  # init empty
        for val in self.key:
            self.key_rots.append(self.ALPHABET.index(val))

        # Key is repeated for length of message:
        tmp_ind = 0
        while len(self.key_rots) <= len(self.msg):
            if tmp_ind > (len(self.key) - 1):
                tmp_ind = 0  # reset ind
            self.key_rots.append(self.key_rots[tmp_ind])
            tmp_ind += 1  # increment

        # And now process each letter of message by rotation
        for ind, val in enumerate(self.msg):
            shifted_ind = self.direction * self.key_rots[ind] + self.ALPHABET.index(val)

            # Deal with overrun:
            if shifted_ind > 25:
                shifted_ind = shifted_ind - 26
            elif shifted_ind < 0:
                shifted_ind = 26 + shifted_ind

            self.output += self.ALPHABET[shifted_ind]

    def print_output (self):
        print(self.output)


# =====================
# Main
# =====================


def main ():
    parser = argparse.ArgumentParser(
        description="Little script to play with Vigenere cipher",
        usage='%(prog)s [encode|decode] [msg] [key]'
    )

    ALLOWED_DIRECTIONS = ["encode", "decode"]

    # Just positional arguments for simplicity, all are required.
    parser.add_argument('direction', nargs='+', help="encryption direction [encode|decode]", type=str)
    parser.add_argument('msg', nargs='+', help="msg to encode|decode", type=str)
    parser.add_argument('key', nargs='+', help="the encryption key", type=str)
    args = parser.parse_args()

    direction = args.direction[0].lower()
    msg = args.msg[0].lower()
    key = args.key[0].lower()

    if direction not in ALLOWED_DIRECTIONS:
        print(f"ERROR: must choose from {ALLOWED_DIRECTIONS}")
        sys.exit(-1)
    elif len(key) > len(msg):
        print(f"ERROR: length of key exceeds length of msg!")
        sys.exit(-1)

    # Init EncoderDecoder Object:
    encoder_decoder = EncoderDecoder(direction, msg, key)
    encoder_decoder.process()
    encoder_decoder.print_output()

    return

# =====================
# Entry Point
# =====================


if __name__ == '__main__':
    main()
