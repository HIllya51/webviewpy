import ctypes

from webviewpy import Webview, webview_native_handle_kind_t
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
)


class WebivewWidget(QWidget):
    def __init__(self, parent=None, debug=False) -> None:
        super().__init__(parent)
        self.webview = Webview(debug=debug, window=int(self.winId()))

        self.webview.bind("__on_load", self.on_load)
        self.webview.init("window.__on_load(window.location)")

    def on_load(self, location):
        print(location)

    def __getattr__(self, name):
        return getattr(self.webview, (name))

    def resizeEvent(self, a0: QResizeEvent) -> None:
        hwnd = self.webview.get_native_handle(
            webview_native_handle_kind_t.WEBVIEW_NATIVE_HANDLE_KIND_UI_WIDGET
        )
        r = QApplication.instance().devicePixelRatio()
        ctypes.windll.User32.MoveWindow(
            hwnd, 0, 0, int(r * a0.size().width()), int(r * a0.size().height()), True
        )


class MyWindow(QWidget):
    def __call_python(self, *arg):
        print(*arg)
        self.setWindowTitle(arg[0])

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.webview = WebivewWidget()
        self.webview.bind("call_python", self.__call_python)
        self.webview.navigate("http://localhost:3000/")
        layout.addWidget(self.webview)
        layout.setContentsMargins(*([0] * 4))
        self.resize(1000, 500)


QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
app = QApplication([])
window = MyWindow()
window.show()
app.exec_()
