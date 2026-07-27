__all__ = ['video_window']

from .VideoWindow import VideoWindow

window: VideoWindow | None = None


def video_window() -> None:
    global window
    if window is None: window = VideoWindow()

    if window.isVisible():
        window.close()
    else:
        window.show()
    pass
