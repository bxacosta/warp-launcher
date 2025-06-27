import sys

if sys.platform != "win32":
    raise RuntimeError("Warp Launcher is only compatible with Windows")
