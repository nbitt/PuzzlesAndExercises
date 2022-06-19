# NOTE:
NOT CURRENTLY WORKING - ISSUE WITH HASH MATH

# OVERVIEW
An obvious re-invention of a very "invented" wheel. This is a python implementation of the md5
hashing algorithm, created as exercise to better understand hashing (& algorithms that underlie
this process). This work leans heavily on the [Wikipedia page] (https://en.wikipedia.org/wiki/MD5),
which contains a helpful overview and block of pseudo code.

# INSTALL
Install with pip by first navigating to the ./md5 directory and then running:

`pip install .`

This will run the setup.py file in the current directory, installing the package for use
from the command line.

# A NOTE ON SECURITY
Md5 is cracked and is no longer considered secure. The number of possible digests is HUGE, but
finite, and there are theoretically an infinite number of inputs that could generate the same
hash (a collision). Bad actors may take advantage of this through a "collision attack." It is
much better to use an alg like SHA-256 for hashing (as of 2021).

# TEST
A limited set of tests can be run by:
1. Navigating to ../test/
2. Running the following:
`python test.py`

