__all__ = ['py_exec_window']

from .PyExecWindow import PyExecWindow

window: PyExecWindow | None = None


def py_exec_window() -> None:
    global window
    if window is None:
        window = PyExecWindow()
        pass
    if window.isVisible():
        window.close()
    else:
        window.show()
    pass
