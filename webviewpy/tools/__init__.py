import os
import platform

import sys


def get_dll_path():
    is_64bit = platform.architecture()[0] == "64bit"
    dll_base_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "platform", sys.platform, ("x86", "x64")[is_64bit]
        )
    )
    if sys.platform == "win32":
        target_dll_name = "webview.dll"
    elif sys.platform == "linux":
        target_dll_name = "libwebview.so"
    elif sys.platform == "darwin":
        target_dll_name = "libwebview.dylib"
    else:
        target_dll_name = "webview"
    return os.path.join(dll_base_path, target_dll_name)
