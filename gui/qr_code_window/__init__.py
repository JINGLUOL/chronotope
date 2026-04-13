__all__ = ['qr_code_window']

from PyQt5.QtWidgets import QWidget

from pyqt.qt5.window import TransparentWindow
from .QRCodeCreator import QRCodeCreator

window: QRCodeCreator | None = None


def qr_code_window(parent: TransparentWindow | QWidget | None = None) -> None:
    global window
    if window is None:
        window = QRCodeCreator(parent)
        if parent: window.setWindowIcon(parent.windowIcon())
        pass
    window.show()
    pass
