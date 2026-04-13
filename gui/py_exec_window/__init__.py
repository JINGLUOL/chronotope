__all__ = ['py_exec_window']

from PyQt5.QtWidgets import QWidget

from pyqt.qt5.window import TransparentWindow
from .PyExecWindow import PyExecWindow

window: PyExecWindow | None = None


def py_exec_window(parent: TransparentWindow | QWidget | None = None) -> None:
    global window
    if window is None:
        window = PyExecWindow(parent)
        if parent: window.setWindowIcon(parent.windowIcon())
        pass
    window.show()
    pass
