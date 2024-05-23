from ctypes import *
from ctypes.wintypes import *
import webviewpy

WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)

WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000

SW_SHOWNORMAL = 1
SW_SHOW = 5

CS_HREDRAW = 2
CS_VREDRAW = 1

CW_USEDEFAULT = 0x80000000

WM_DESTROY = 2

WHITE_BRUSH = 0


class WNDCLASSEX(Structure):
    _fields_ = [("cbSize", c_uint),
                ("style", c_uint),
                ("lpfnWndProc", WNDPROCTYPE),
                ("cbClsExtra", c_int),
                ("cbWndExtra", c_int),
                ("hInstance", HANDLE),
                ("hIcon", HANDLE),
                ("hCursor", HANDLE),
                ("hBrush", HANDLE),
                ("lpszMenuName", LPCWSTR),
                ("lpszClassName", LPCWSTR),
                ("hIconSm", HANDLE)]

user32 = windll.user32
user32.DefWindowProcW.argtypes = [HWND, c_uint, WPARAM, LPARAM]

def PyWndProcedure(hWnd, Msg, wParam, lParam):
    if Msg == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0
    # when try init webview here too, but it raise exception
    # i think its due to initialization on the backgroud thread issue
    return user32.DefWindowProcW(hWnd, Msg, wParam, lParam)

def resizewebview(webview):
    hwnd = webview.get_native_handle(
        webviewpy.webview_native_handle_kind_t.WEBVIEW_NATIVE_HANDLE_KIND_UI_WIDGET
    )
    r = RECT()
    if windll.user32.GetClientRect(windll.user32.GetParent(hwnd), pointer(r)):

        windll.User32.MoveWindow(
            hwnd, r.left, r.top, r.right - r.left, r.bottom - r.top, True
        )

def main():
    WndProc = WNDPROCTYPE(PyWndProcedure)
    hInst = windll.kernel32.GetModuleHandleW(0)
    wclassName = u'test window'
    wname = u'test window'
    
    wndClass = WNDCLASSEX()
    wndClass.cbSize = sizeof(WNDCLASSEX)
    wndClass.style = CS_HREDRAW | CS_VREDRAW
    wndClass.lpfnWndProc = WndProc
    wndClass.cbClsExtra = 0
    wndClass.cbWndExtra = 0
    wndClass.hInstance = hInst
    wndClass.hIcon = 0
    wndClass.hCursor = 0
    wndClass.hBrush = windll.gdi32.GetStockObject(WHITE_BRUSH)
    wndClass.lpszMenuName = 0
    wndClass.lpszClassName = wclassName
    wndClass.hIconSm = 0
    
    windll.user32.RegisterClassExW(byref(wndClass))
    
    hWnd = windll.user32.CreateWindowExW(
    0, wclassName, wname,
    WS_OVERLAPPEDWINDOW | WS_CAPTION,
    CW_USEDEFAULT, CW_USEDEFAULT,
    1200, 700, 0, 0, hInst, 0)
    
    if not hWnd:
        print('Failed to create window')
        exit(0)
        
    windll.user32.ShowWindow(hWnd, SW_SHOW)
    windll.user32.UpdateWindow(hWnd)

    webview = webviewpy.Webview(debug=False, window=hWnd)
    resizewebview(webview)
    webview.set_html("<div>test content<div>")
    webview.run()
    
    
if __name__ == "__main__":
    print ("Win32 Application in python")
    main()