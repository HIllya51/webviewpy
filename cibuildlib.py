import sys,subprocess,shutil,os
print(sys.platform)
def listdir():
    for f in os.walk('.'):
        _dir,_,_fs=f
        for _f in _fs:
            print(os.path.abspath(os.path.join(_dir,_f)))
if sys.argv[1]=='release':
    os.makedirs('./wheel')
    listdir()
    filepath=os.path.dirname(__file__)
    os.chdir(filepath)
    copy=lambda f,d:os.makedirs(d) or shutil.copy(f,d)
    copy('./build/windows-2019x86/library/webview.dll','./webviewpy/platform/win32/x86')
    copy('./build/windows-2019x64/library/webview.dll','./webviewpy/platform/win32/x64')
    #copy('./build/ubuntu-20.04x86/library/libwebview.so','./webviewpy/platform/linux/x86')
    copy('./build/ubuntu-20.04x64/library/libwebview.so','./webviewpy/platform/linux/x64')
    #copy('./build/macos-11x86/library/libwebview.dylib','./webviewpy/platform/darwin/x86')
    copy('./build/macos-11x64/library/libwebview.dylib','./webviewpy/platform/darwin/x64')
    os.system('python -m build')
    listdir()
    exit()

arch=sys.argv[1]
curr=os.getcwd()
print(curr)
os.chdir(f'{curr}/webview')
os.makedirs(f'{curr}/platform/{sys.platform}')
os.makedirs(f'{curr}/platform/{sys.platform}/x86')
os.makedirs(f'{curr}/platform/{sys.platform}/x64')
if sys.platform=='win32':
    subprocess.run(f"cmd /c set TARGET_ARCH={arch} & call script/build.bat")
    #shutil.move(f"{curr}/webview/build/library/webview.dll", f"{curr}/platform/{sys.platform}/x86")
    #subprocess.run(f"cmd /c set TARGET_ARCH=x64 & call script/build.bat")
    #shutil.move(f"{curr}/webview/build/library/webview.dll", f"{curr}/platform/{sys.platform}/x64")
elif sys.platform=='linux':
    os.system('''
sudo update-alternatives --force --install /usr/bin/gcc gcc /usr/bin/gcc-12 1200 --slave /usr/bin/g++ g++ /usr/bin/g++-12
sudo update-alternatives --remove-all clang
sudo update-alternatives --remove-all clang++
sudo update-alternatives --remove-all clang-format
sudo update-alternatives --remove-all clang-tidy
sudo update-alternatives --force --install /usr/bin/clang clang /usr/bin/clang-15 1500 --slave /usr/bin/clang++ clang++ /usr/bin/clang++-15 --slave /usr/bin/clang-format clang-format /usr/bin/clang-format-15 --slave /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-15
sudo apt-get update && sudo apt-get install libwebkit2gtk-4.0-dev xvfb -y
''')
    os.system(f"export TARGET_ARCH={arch} & xvfb-run script/build.sh build")
    #listdir()
    #shutil.move(f"{curr}/webview/build/library/libwebview.so", f"{curr}/platform/{sys.platform}/x86")
    #os.system(f"export TARGET_ARCH=x64 & xvfb-run script/build.sh build")
    #shutil.move(f"{curr}/webview/build/library/libwebview.so", f"{curr}/platform/{sys.platform}/x64")
elif sys.platform=='darwin':
    os.system(f"export TARGET_ARCH={arch} & script/build.sh build")
    #listdir()
    #shutil.move(f"{curr}/webview/build/library/libwebview.dylib", f"{curr}/platform/{sys.platform}/x86")
    #os.system(f"export TARGET_ARCH=x64 & script/build.sh build")
    #shutil.move(f"{curr}/webview/build/library/libwebview.dylib", f"{curr}/platform/{sys.platform}/x64")
os.chdir(curr)
