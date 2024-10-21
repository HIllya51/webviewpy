import sys, subprocess, shutil, os

print(sys.platform)


def listdir():
    for f in os.walk("."):
        _dir, _, _fs = f
        for _f in _fs:
            print(os.path.abspath(os.path.join(_dir, _f)))


if len(sys.argv) >= 2 and sys.argv[1] == "release":
    os.makedirs("./wheel", exist_ok=True)
    listdir()
    filepath = os.path.dirname(__file__)
    os.chdir(filepath)
    copy = (
        lambda f, d: print(os.path.exists(f), os.path.abspath(f), os.path.abspath(d))
        or os.makedirs(d, exist_ok=True)
        or shutil.copy(f, d)
    )

    copy("./build/windows-2022/x86/bin/Release/webview.dll", "./webviewpy/platform/win32/x86")
    copy("./build/windows-2022/x64/bin/Release/webview.dll", "./webviewpy/platform/win32/x64")
    # copy('./build/ubuntu-20.04x86/library/libwebview.so','./webviewpy/platform/linux/x86')
    copy(
        "./build/ubuntu-22.04/x64/lib/libwebview.so",
        "./webviewpy/platform/linux/x64",
    )
    # copy('./build/macos-11x86/library/libwebview.dylib','./webviewpy/platform/darwin/x86')
    copy(
        "./build/macos-14/x64/lib/libwebview.dylib",
        "./webviewpy/platform/darwin/x64",
    )
    os.system("python -m build")
    listdir()
    exit()

curr = os.getcwd()
print(curr)
if sys.platform == "win32":
    os.system("cmake -A win32 -T host=x86 -B ./build/x86")
    os.system("cmake --build ./build/x86 --config Release --target ALL_BUILD")

    os.system("cmake -A x64 -T host=x64 -B ./build/x64")
    os.system("cmake --build ./build/x64 --config Release --target ALL_BUILD")
elif sys.platform == "linux":
    os.system(
        """
sudo update-alternatives --force --install /usr/bin/gcc gcc /usr/bin/gcc-12 1200 --slave /usr/bin/g++ g++ /usr/bin/g++-12
sudo update-alternatives --remove-all clang
sudo update-alternatives --remove-all clang++
sudo update-alternatives --remove-all clang-format
sudo update-alternatives --remove-all clang-tidy
sudo update-alternatives --force --install /usr/bin/clang clang /usr/bin/clang-15 1500 --slave /usr/bin/clang++ clang++ /usr/bin/clang++-15 --slave /usr/bin/clang-format clang-format /usr/bin/clang-format-15 --slave /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-15
sudo apt-get update && sudo apt-get install libwebkit2gtk-4.0-dev xvfb -y
"""
    )
    os.system("cmake -B ./build/x64")
    os.system("cmake --build ./build/x64 --config Release")
elif sys.platform == "darwin":
    os.system("cmake -B ./build/x64")
    os.system("cmake --build ./build/x64 --config Release")
os.chdir(curr)
