__all__ = ['py_exec_window']

from .PyExecWindow import PyExecWindow

window: PyExecWindow | None = None


def py_exec_window(parent=None) -> None:
    global window
    if window is None:
        window = PyExecWindow()
        if parent: window.setWindowIcon(parent.windowIcon())
        pass
    if window.isVisible():
        window.close()
    else:
        window.show()
    pass
