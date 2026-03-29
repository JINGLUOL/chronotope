__all__ = [
    'create_octaves3_piano',
    'create_octaves5_piano',
    'create_octaves7_piano',

    'piano_toggle_visibility',

    'set_difficulty_to_none',
    'set_difficulty_to_easy',
    'set_difficulty_to_hard',
    'set_difficulty_to_hell',

    'delete_piano_window'
]

from pyqt.qt5.window import TransparentWindow
from .PianoWindow import PianoWindow, PracticeLevel

piano_window: PianoWindow | None = None


def create_piano_window(parent: TransparentWindow, octaves: int) -> PianoWindow:
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


def create_octaves3_piano(parent: TransparentWindow):
    create_piano_window(parent, 3).show()


def create_octaves5_piano(parent: TransparentWindow):
    create_piano_window(parent, 5).show()


def create_octaves7_piano(parent: TransparentWindow):
    create_piano_window(parent, 7).show()


def piano_toggle_visibility():
    global piano_window
    if piano_window:
        piano_window.toggle_visibility()
        pass
    pass


def set_difficulty_to_none():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.NONE)
        pass
    pass


def set_difficulty_to_easy():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.EASY)
        pass
    pass


def set_difficulty_to_normal():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.NORMAL)
        pass
    pass


def set_difficulty_to_hard():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.HARD)
        pass
    pass


def set_difficulty_to_hell():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.HELL)
        pass
    pass


def delete_piano_window():
    global piano_window
    if piano_window:
        piano_window.destroy()
        piano_window = None
        pass
    pass
