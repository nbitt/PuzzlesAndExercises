"""
Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts
for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least
five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given
below) followed by a number in decimal. To mine AdventCoins, you must find Santa the
lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.
"""

import argparse
import hashlib
import time

def main (secret_key):
    i = 1  # init prefix value (no leading zeros)
    secret_key = bytes(secret_key, 'utf-8')

    # start = time.time()  # only for timing


    while True:
        md5 = hashlib.md5()
        md5.update(secret_key + str(i).encode())  # converts to bytes
        digest = md5.hexdigest()
        if digest[0:6] == '000000':
            print(digest)
            print(i)

            # only for timing (NOTE: TIMING VALUES ARE FISHY)
            #print(time.time() - start)
            # PREFIX  | i        | time (sec)
            # '0'     | 4        | 9.083747863769531e-05
            # '00'    | 524      | 0.002682209014892578
            # '000'   | 1866     | 0.011358976364135742
            # '0000'  | 43159    | 2.1244561672210693
            # '00000' | 454532   | 7 min < t < 10 min
            # 5*4 = 20 leading zeros...

            # attempts = 0.5874 * e ** 2.7693 * bit_num
            # R^2 = 0.96895
            # NOTE: time does not map linearly with attempts vs time
            # Longer hashes = harder.

            break
        i += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('secret_key', type=str, help="Secret Key (see challenge descr.)")
    args = parser.parse_args()
    main(args.secret_key)
