__all__ = ['video_window']

from .VideoWindow import VideoWindow

window: VideoWindow | None = None


def video_window(parent=None) -> None:
    global window
    if window is None:
        window = VideoWindow(parent)
        if parent: window.setWindowIcon(parent.windowIcon())
        pass
    window.show()
    pass
