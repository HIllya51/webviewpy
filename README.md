# webviewpy

A tiny webview library for Python.

Based on [webview](https://github.com/webview/webview)


# Getting started

### Install


``` bash
pip install webviewpy
```


### Usage

[Build a webview based app](example/test.py)

[Embed a webview in PyQt](example/testpyqt.py)

[Embed a webview in tkinter](example/testtkinter.py)


[Build a webview based app with react and PyQt](example/fluent/main.py)


### Specify library path


Wheel includes pre-built libraries of Windows/Linux/Macos, and libraries are placed at platform/{sys.platform}/{x86|x64}/webview. 

To specify a self-built library or use other platform's library, use api ```declare_library_path``` like this:

``` python
from webviewpy import declare_library_path
declare_library_path(
    r"C:\build\library\webview.dll"
)
```
