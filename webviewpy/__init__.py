import platform, os, sys, json, functools
from ctypes import (
    CDLL,
    c_int,
    c_void_p,
    c_char_p,
    Structure,
    c_uint,
    c_char,
    POINTER,
    CFUNCTYPE,
    cast,
)


class webview_t(c_void_p):
    pass


# Window size hints
class webview_hint_t(c_int):
    # Width and height are default size.
    WEBVIEW_HINT_NONE = 0
    # Width and height are minimum bounds.
    WEBVIEW_HINT_MIN = 1
    # Width and height are maximum bounds.
    WEBVIEW_HINT_MAX = 2
    # Window size can not be changed by a user.
    WEBVIEW_HINT_FIXED = 3


class webview_error_t(c_int):
    # Missing dependency.
    WEBVIEW_ERROR_MISSING_DEPENDENCY = -5
    # Operation canceled.
    WEBVIEW_ERROR_CANCELED = -4
    # Invalid state detected.
    WEBVIEW_ERROR_INVALID_STATE = -3
    # One or more invalid arguments have been specified e.g. in a function call.
    WEBVIEW_ERROR_INVALID_ARGUMENT = -2
    # An unspecified error occurred. A more specific error code may be needed.
    WEBVIEW_ERROR_UNSPECIFIED = -1
    # OK/Success. Functions that return error codes will typically return this
    # to signify successful operations.
    WEBVIEW_ERROR_OK = 0
    # Signifies that something already exists.
    WEBVIEW_ERROR_DUPLICATE = 1
    # Signifies that something does not exist.
    WEBVIEW_ERROR_NOT_FOUND = 2


# Native handle kind. The actual type depends on the backend.
class webview_native_handle_kind_t(c_int):

    # Top-level window. @c GtkWindow pointer (GTK), @c NSWindow pointer (Cocoa)
    # or @c HWND (Win32).
    WEBVIEW_NATIVE_HANDLE_KIND_UI_WINDOW = 0
    # Browser widget. @c GtkWidget pointer (GTK), @c NSView pointer (Cocoa) or
    # @c HWND (Win32).
    WEBVIEW_NATIVE_HANDLE_KIND_UI_WIDGET = 1
    # Browser controller. @c WebKitWebView pointer (WebKitGTK), @c WKWebView
    # pointer (Cocoa/WebKit) or @c ICoreWebView2Controller pointer
    # (Win32/WebView2).
    WEBVIEW_NATIVE_HANDLE_KIND_BROWSER_CONTROLLER = 2


class webview_version_t(Structure):
    _fields_ = [("major", c_uint), ("minor", c_uint), ("patch", c_uint)]


class webview_version_info_t(Structure):
    _fields_ = [
        ("version", webview_version_t),
        ("version_number", c_char * 32),
        ("pre_release", c_char * 48),
        ("build_metadata", c_char * 48),
    ]


class _Webview_Version:
    def __init__(self, v: webview_version_t) -> None:
        self.major = v.major
        self.minor = v.minor
        self.patch = v.patch

    def __repr__(self) -> str:
        return "{}.{}.{}".format(self.major, self.minor, self.patch)


class Webview_Version:
    def __repr__(self) -> str:
        return self.version_number

    def __init__(self, lpwv) -> None:
        self.version = _Webview_Version(lpwv.contents.version)
        self.version_number = lpwv.contents.version_number.decode("utf8")
        self.pre_release = lpwv.contents.pre_release.decode("utf8")
        self.build_metadata = lpwv.contents.build_metadata.decode("utf8")


class webview_exception(Exception):
    pass


def get_library_path():
    is_64bit = platform.architecture()[0] == "64bit"
    library_base_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "platform", sys.platform, ("x86", "x64")[is_64bit]
        )
    )
    if sys.platform == "win32":
        target_library_name = "webview.dll"
    elif sys.platform == "linux":
        target_library_name = "libwebview.so"
    elif sys.platform == "darwin":
        target_library_name = "libwebview.dylib"
    else:
        target_library_name = "webview"
    return os.path.join(library_base_path, target_library_name)

webviewdll = get_library_path()


webview_dispatch_fn_t = CFUNCTYPE(None, webview_t, c_void_p)
webview_bind_fn_t = CFUNCTYPE(None, c_char_p, c_char_p, c_void_p)


def declare_library_path(librarypath=None, exception=True):
    if librarypath is None:
        librarypath = webviewdll
    try:
        global is_webviewlibrary_load_ok
        is_webviewlibrary_load_ok = False
        _webview = CDLL(librarypath)
        webview_create = _webview.webview_create
        webview_create.argtypes = c_int, c_void_p
        webview_create.restype = webview_t
        webview_set_title = _webview.webview_set_title
        webview_set_title.argtypes = webview_t, c_char_p
        webview_set_title.restype = webview_error_t
        webview_set_size = _webview.webview_set_size
        webview_set_size.argtypes = webview_t, c_int, c_int, webview_hint_t
        webview_set_size.restype = webview_error_t
        webview_set_html = _webview.webview_set_html
        webview_set_html.argtypes = webview_t, c_char_p
        webview_set_html.restype = webview_error_t
        webview_run = _webview.webview_run
        webview_run.argtypes = (webview_t,)
        webview_run.restype = webview_error_t
        webview_destroy = _webview.webview_destroy
        webview_destroy.argtypes = (webview_t,)
        webview_destroy.restype = webview_error_t
        webview_navigate = _webview.webview_navigate
        webview_navigate.argtypes = webview_t, c_char_p
        webview_navigate.restype = webview_error_t
        webview_eval = _webview.webview_eval
        webview_eval.argtypes = webview_t, c_char_p
        webview_eval.restype = webview_error_t
        webview_get_window = _webview.webview_get_window
        webview_get_window.argtypes = (webview_t,)
        webview_get_window.restype = c_void_p
        webview_get_native_handle = _webview.webview_get_native_handle
        webview_get_native_handle.argtypes = webview_t, webview_native_handle_kind_t
        webview_get_native_handle.restype = c_void_p
        webview_init = _webview.webview_init
        webview_init.argtypes = webview_t, c_char_p
        webview_init.restype = webview_error_t
        webview_version = _webview.webview_version
        webview_version.restype = POINTER(webview_version_info_t)
        webview_terminate = _webview.webview_terminate
        webview_terminate.argtypes = (webview_t,)
        webview_terminate.restype = webview_error_t
        webview_unbind = _webview.webview_unbind
        webview_unbind.argtypes = webview_t, c_char_p
        webview_unbind.restype = webview_error_t

        webview_return = _webview.webview_return
        webview_return.argtypes = webview_t, c_char_p, c_int, c_char_p
        webview_return.restype = webview_error_t
        webview_dispatch = _webview.webview_dispatch
        webview_dispatch.argtypes = webview_t, c_void_p, c_void_p
        webview_dispatch.restype = webview_error_t
        webview_bind = _webview.webview_bind
        webview_bind.argtypes = webview_t, c_char_p, c_void_p, c_void_p
        webview_bind.restype = webview_error_t

        is_webviewlibrary_load_ok = True
        variables = locals()
        globals().update(variables)
    except:
        log = 'load module "{}" failed'.format(librarypath)
        if exception:
            raise webview_exception(log)


declare_library_path(None, False)


class Webview:

    def __new__(cls, *args, **kwargs):
        global is_webviewlibrary_load_ok
        if not is_webviewlibrary_load_ok:
            raise webview_exception("webview library not loaded")
        instance = super().__new__(cls)
        return instance

    def __init__(self, debug=False, window=None):

        self.pwebview = None
        _w = webview_create(debug, window)
        if _w.value is None:
            raise webview_exception("create webview failed")
        self.pwebview = _w
        self.keepref = []

    def resolve(self, id, status, result):
        return webview_return(
            self.pwebview, id.encode("utf8"), status, result.encode("utf8")
        )

    def bind(
        self,
        name,
        fn,
        is_async_return=False,
    ):
        def wrapped_fn(is_async_return, seq, req, args):
            seq = seq.decode("utf8")

            if is_async_return:

                def returner(seq, *args):
                    self.resolve(seq, 0, json.dumps(args))

                _returner = functools.partial(returner, seq)
                _result = fn(_returner, *json.loads(req.decode("utf8")))

            else:
                _result = fn(*json.loads(req.decode("utf8")))
                result = json.dumps(_result)
                self.resolve(seq, 0, result)

        _funcptr = webview_bind_fn_t(functools.partial(wrapped_fn, is_async_return))
        self.keepref.append(_funcptr)
        return webview_bind(
            self.pwebview,
            name.encode("utf8"),
            cast(_funcptr, c_void_p).value,
            None,
        )

    def dispatch(self, fn):
        def wrapped_fn(_w, _arg):
            fn()

        _funcptr = webview_dispatch_fn_t(wrapped_fn)
        self.keepref.append(_funcptr)
        return webview_dispatch(self.pwebview, cast(_funcptr, c_void_p).value, None)

    def unbind(self, name):
        return webview_unbind(self.pwebview, name.encode("utf8"))

    def get_window(self):
        return webview_get_window(self.pwebview)

    def get_native_handle(self, kind):
        return webview_get_native_handle(self.pwebview, kind)

    def eval(self, js):
        return webview_eval(self.pwebview, js.encode("utf8"))

    def navigate(self, url):
        return webview_navigate(self.pwebview, url.encode("utf8"))

    def init(self, js):
        return webview_init(self.pwebview, js.encode("utf8"))

    def destroy(self):
        if self.pwebview:
            _ = webview_destroy(self.pwebview)
            self.pwebview = None
            return _
        else:
            return webview_error_t.WEBVIEW_ERROR_OK

    def __del__(self) -> None:
        self.destroy()

    def run(self):
        return webview_run(self.pwebview)

    def set_html(self, html):
        return webview_set_html(self.pwebview, html.encode("utf8"))

    def set_size(
        self,
        width,
        height,
        hints=webview_hint_t.WEBVIEW_HINT_NONE,
    ):
        return webview_set_size(self.pwebview, width, height, hints)

    def set_title(self, title):
        return webview_set_title(self.pwebview, title.encode("utf8"))

    def terminate(self):
        return webview_terminate(self.pwebview)

    @staticmethod
    def version():
        return Webview_Version(webview_version())


__all__ = [
    getattr(_, "__name__")
    for _ in [
        get_library_path,
        declare_library_path,
        webview_hint_t,
        webview_error_t,
        webview_native_handle_kind_t,
        webview_exception,
        Webview,
    ]
]
