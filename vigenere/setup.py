import re
from distutils.core import setup

# version import based on: https://github.com/tahoe-lafs/zfec
VERSIONFILE = os.path.join(PKG, "_version.py")
verstr = "unknown"

try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass
else:
    VSRE = r"^verstr = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print(f"unable to find version in {VERSIONFILE}")
        raise RuntimeError("if %s.py exists, it is required to be well-formed" % (VERSIONFILE,))
