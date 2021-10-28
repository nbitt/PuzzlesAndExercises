"""

A quick little class and method to explore recursive vs
iterative algorithms, based on reading from wikipedia.

Notes:
    > Iterative actually appears to be a bit quicker for most integers <1000
    (~0.0009 secs faster)
    > Recursion error occurs with values >997

"""

# IMPORTS
import argparse
import sys
import time
from sys import exit


def recursive_factorial (input_int):
    # Recurse :) (try to make equiv as possible)

    if input_int == 1:
        return 1
    else:
        # n * (n-1 * (n - 2) .. etc)
        return input_int * recursive_factorial(input_int - 1)


def iterative_factorial (input_int):
    output = input_int  # try to make equiv as possible (no "range())
    i = input_int - 1

    # Iterate! :)
    while i > 0:
        output = output * i
        i -= 1

    return output

# MAIN
def main (val_int):

    # Recursive:
    start = time.time()
    recursive_out = recursive_factorial(val_int)
    recursive_secs = time.time() - start

    # Iterative:
    start = time.time()
    iterative_out = iterative_factorial(val_int)
    iterative_secs = time.time() - start

    if iterative_out != recursive_out:
        print(f"ERROR: recursive: {recursive_out} does not match iterative: {iterative_out}")
        sys.exit(-1)
    print(f"Factorial: {iterative_out}")

    time_diff = iterative_secs - recursive_secs  # units seconds

    if time_diff == 0:
        print('Algs took precisely the same time')
    elif time_diff < 0:
        print(f"Iterative alg was faster by {abs(time_diff)} secs")
    elif time_diff > 0:
        print(f"Recursive alg was faster by {time_diff} secs")


# ENTRY POINT
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Calculate (and time)",
        usage="python %(prog)s <integer value>",
    )
    parser.add_argument('val_int', type=int, help="integer against which to calc factorial")
    args = parser.parse_args()
    if type(args.val_int) != int:
        print(f"ERROR: input must be integer!")
        sys.exit(-1)

    main(args.val_int)



