import os, sys, ctypes

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from webviewpy import Webview, webview_native_handle_kind_t
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)

testQWebEngineView = False


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


if testQWebEngineView:
    from PyQt5.QtWebEngineWidgets import QWebEngineView


class MyWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QPushButton("navigate")
        edit = QLineEdit("https://www.bilibili.com/")
        if testQWebEngineView:
            self.webview = QWebEngineView()
            self.webview.load(QUrl("https://www.baidu.com/"))
            btn.clicked.connect(lambda _: self.webview.load(QUrl(edit.text())))
        else:
            self.webview = WebivewWidget()
            self.webview.navigate("https://www.baidu.com/")
            btn.clicked.connect(lambda _: self.webview.navigate(edit.text()))
        hl = QHBoxLayout()
        hl.addWidget(edit)
        hl.addWidget(btn)
        layout.addLayout(hl)
        layout.addWidget(self.webview)

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
