import tkinter as tk
import ctypes
from webviewpy import *

webview = None


def on_resize(event):
    global webview

    if webview is None:
        webview = Webview(debug=False, window=window.winfo_id())
        webview.navigate("https://www.baidu.com/")

    if str(event.widget) == ".":
        width = event.width
        height = event.height
        hwnd = webview.get_native_handle(
            webview_native_handle_kind_t.WEBVIEW_NATIVE_HANDLE_KIND_UI_WIDGET
        )
        ctypes.windll.User32.MoveWindow(hwnd, 0, 30, width, height - 30, True)


def on_button_click():
    global webview
    webview.navigate("https://www.bilibili.com")
    webview.eval('alert("shit!")')


window = tk.Tk()
window.bind("<Configure>", on_resize)
window.geometry("400x300")
button = tk.Button(window, text="click", command=on_button_click)
button.pack()

window.mainloop()
