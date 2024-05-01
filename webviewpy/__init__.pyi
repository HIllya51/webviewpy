from ctypes import (
    c_int,
    c_void_p,
)
from typing import Callable, Union, TypeVar, Optional

SerializableType = TypeVar("SerializableType")

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


class Webview_Version:
    ...


class webview_exception(Exception):
    pass


def declare_library_path(librarypath=None, exception=True):
    ...

class Webview:

    def __init__(self, debug: bool = False, window: c_void_p = None) -> None:
        """
        * Creates a new webview instance.
        *
        * @param debug Enable developer tools if supported by the backend.
        * @param window Optional native window handle, i.e. @c GtkWindow pointer
        *        @c NSWindow pointer (Cocoa) or @c HWND (Win32). If non-null,
        *        the webview widget is embedded into the given window, and the
        *        caller is expected to assume responsibility for the window as
        *        well as application lifecycle. If the window handle is null,
        *        a new window is created and both the window and application
        *        lifecycle are managed by the webview instance.
        * @remark Win32: The function also accepts a pointer to @c HWND (Win32) in the
        *         window parameter for backward compatibility.
        * @remark Win32/WebView2: @c CoInitializeEx should be called with
        *         @c COINIT_APARTMENTTHREADED before attempting to call this function
        *         with an existing window. Omitting this step may cause WebView2
        *         initialization to fail.
        * @return Webview object.
        """
        ...

    def resolve(self, id: str, status: int, result: str) -> webview_error_t:
        """
        * Responds to a binding call from the JS side.
        *
        * @param id The identifier of the binding call. Pass along the value received
        *           in the binding handler (see webview_bind()).
        * @param status A status of zero tells the JS side that the binding call was
        *               succesful; any other value indicates an error.
        * @param result The result of the binding call to be returned to the JS side.
        *               This must either be a valid JSON value or an empty string for
        *               the primitive JS value @c undefined.
        """
        ...

    def bind(
        self,
        name: str,
        fn: Callable[
            [
                Optional[Callable[SerializableType, None]],
                ...,
            ],
            Union[None, SerializableType],
        ],
        is_async_return=False,
    ) -> webview_error_t:
        """
        * Binds a function pointer to a new global JavaScript function.
        *
        * Internally, JS glue code is injected to create the JS function by the
        * given name. The callback function is passed a request identifier,
        * a request string and a user-provided argument. The request string is
        * a JSON array of the arguments passed to the JS function.
        *
        * @param name Name of the JS function.
        * @param fn Callback function.
        * @param arg User argument.
        * @retval WEBVIEW_ERROR_DUPLICATE
        *         A binding already exists with the specified name.
        """
        ...

    def dispatch(self, fn: Callable[[], None]) -> webview_error_t:
        """
        * Schedules a function to be invoked on the thread with the run/event loop.
        * Use this function e.g. to interact with the library or native handles.
        *
        * @param fn The function to be invoked.
        * @param arg An optional argument passed along to the callback function.
        """
        ...
    def unbind(self, name: str) -> webview_error_t:
        """
        * Removes a binding created with webview_bind().
        *
        * @param name Name of the binding.
        * @retval WEBVIEW_ERROR_NOT_FOUND No binding exists with the specified name.
        """
        ...

    def get_window(self) -> c_void_p:
        """
        * Returns the native handle of the window associated with the webview instance.
        * The handle can be a @c GtkWindow pointer (GTK), @c NSWindow pointer (Cocoa)
        * or @c HWND (Win32).
        *
        * @return The handle of the native window.
        """
        ...

    def get_native_handle(self, kind: webview_native_handle_kind_t) -> c_void_p:
        """
        * Get a native handle of choice.
        *
        * @param kind The kind of handle to retrieve.
        * @return The native handle or @c NULL.
        * @since 0.11
        """
        ...

    def eval(self, js: str) -> webview_error_t:
        """
        * Evaluates arbitrary JavaScript code.
        *
        * Use bindings if you need to communicate the result of the evaluation.
        *
        * @param js JS content.
        """
        ...

    def navigate(self, url: str) -> webview_error_t:
        """
        * Navigates webview to the given URL. URL may be a properly encoded data URI.
        *
        * Example:
        * @code{.c}
        * webview_navigate(w, "https://github.com/webview/webview");
        * webview_navigate(w, "data:text/html,%3Ch1%3EHello%3C%2Fh1%3E");
        * webview_navigate(w, "data:text/html;base64,PGgxPkhlbGxvPC9oMT4=");
        * @endcode
        *
        * @param url URL.
        """
        ...

    def init(self, js: str) -> webview_error_t:
        """
        * Injects JavaScript code to be executed immediately upon loading a page.
        * The code will be executed before @c window.onload.
        *
        * @param js JS content.
        """
        ...

    def destroy(self) -> webview_error_t:
        """
        * Destroys a webview instance and closes the native window.
        """
        ...

    def __del__(self) -> None:
        ...

    def run(self) -> webview_error_t:
        """
        * Runs the main loop until it's terminated.
        """
        ...

    def set_html(self, html: str) -> webview_error_t:
        """
        * Load HTML content into the webview.
        *
        * Example:
        * @code{.c}
        * webview_set_html(w, "<h1>Hello</h1>");
        * @endcode
        *
        * @param html HTML content.
        """
        ...

    def set_size(
        self,
        width: int,
        height: int,
        hints: webview_hint_t = webview_hint_t.WEBVIEW_HINT_NONE,
    ) -> webview_error_t:
        """
        * Updates the size of the native window.
        *
        * @param width New width.
        * @param height New height.
        * @param hints Size hints.
        """
        ...

    def set_title(self, title: str) -> webview_error_t:
        """
        * Updates the title of the native window.
        *
        * @param title The new title.
        """
        ...

    def terminate(self) -> webview_error_t:
        """
        * Stops the main loop. It is safe to call this function from another other
        * background thread.
        """
        ...

    @staticmethod
    def version() -> Webview_Version:
        """
        * Get the library's version information.
        """
        ...

