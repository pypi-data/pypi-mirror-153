import sys
from pathlib import Path
from platform import system

from tukaan._tcl import Tcl


def load_serif() -> None:
    os = {"Linux": "linux", "Darwin": "mac", "Windows": "windows"}[system()]

    if sys.maxsize > 2**32:
        os += "_x64"
    else:
        os += "_x32"

    libfilename = "serif_" + os + Tcl.call(str, "info", "sharedlibextension")
    Tcl.call(None, "load", Path(__file__).parent / "pkg" / libfilename, "Serif")
