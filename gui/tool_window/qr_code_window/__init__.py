__all__ = ['qr_code_window']

from .QRCodeCreator import QRCodeCreator

window: QRCodeCreator | None = None


def qr_code_window() -> None:
    global window
    if window is None:
        window = QRCodeCreator()
        pass
    if window.isVisible():
        window.close()
    else:
        window.show()
    pass
