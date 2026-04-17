__all__ = [
    'create_piano',

    'piano_toggle_visibility',

    'PracticeLevel',
    'set_difficulty',

    'delete_piano_window'
]

from pyqt.qt5.window import TransparentWindow
from .PianoWindow import PianoWindow, PracticeLevel

piano_window: PianoWindow | None = None


def create_piano_window(parent: TransparentWindow, octaves: int = 3) -> PianoWindow:
    global piano_window
    if piano_window:
        if piano_window.octaves == octaves:
            return piano_window
        else:
            piano_window.destroy()
            pass
        pass
    piano_window = PianoWindow(parent.x(), parent.y(), parent.width(), parent.height(), octaves)
    return piano_window


def create_piano(parent: TransparentWindow, octaves: int = 3) -> None:
    create_piano_window(parent, octaves).show()
    pass


def set_difficulty(parent: TransparentWindow, difficulty: PracticeLevel = PracticeLevel.NONE) -> None:
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(difficulty)
        pass
    pass


def piano_toggle_visibility():
    global piano_window
    if piano_window:
        piano_window.toggle_visibility()
        pass
    pass


def delete_piano_window():
    global piano_window
    if piano_window:
        piano_window.destroy()
        piano_window = None
        pass
    pass
