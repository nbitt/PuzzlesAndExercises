# =====================
# IMPORTS
# =====================
import re
from setuptools import setup

# =====================
# PARSE VERSION INFO
# =====================
# version import based on: https://github.com/tahoe-lafs/zfec
VERSIONFILE = "cryptography/_version.py"
verstr = "unknown"

try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass
else:
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print(f"unable to find version in {VERSIONFILE}")
        raise RuntimeError("if %s exists, it is required to be well-formed" % (VERSIONFILE,))

# =====================
# SETUP
# =====================
setup(
    name="vigenere",
    author="nbitt",
    version=verstr,
    packages=['vigenere'],
    entry_points={
        'console_scripts': [
            'vigenere = vigenere.vigenere:main',
        ]
    }
)
