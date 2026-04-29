__all__ = ['py_exec_window']

from .PyExecWindow import PyExecWindow

window: PyExecWindow | None = None


def py_exec_window(parent=None) -> None:
    global window
    if window is None:
        window = PyExecWindow(parent)
        if parent: window.setWindowIcon(parent.windowIcon())
        pass
    window.show()
    pass
