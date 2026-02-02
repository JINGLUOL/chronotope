from global_manager import screen
from .PianoWindow import PianoWindow, PracticeLevel

piano_window: PianoWindow | None = None


def create_piano_window(x: int, y: int, w: int, h: int, octaves: int) -> PianoWindow:
    global piano_window
    if piano_window:
        if piano_window.octaves == octaves:
            return piano_window
        else:
            piano_window.destroy()
            pass
        pass
    piano_window = PianoWindow(x, y, w, h, octaves)
    return piano_window


def create_octaves3_piano():
    create_piano_window(screen.x, screen.y, screen.width, screen.height, 3).show()


def create_octaves5_piano():
    create_piano_window(screen.x, screen.y, screen.width, screen.height, 5).show()


def create_octaves7_piano():
    create_piano_window(screen.x, screen.y, screen.width, screen.height, 7).show()


def piano_toggle_visibility():
    global piano_window
    if piano_window:
        piano_window.toggle_visibility()
    else:
        create_octaves3_piano()
    pass


def piano_practice_difficulty_to_none():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.NONE)
        pass
    pass


def piano_practice_difficulty_to_easy():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.EASY)
        pass
    pass


def piano_practice_difficulty_to_normal():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.NORMAL)
        pass
    pass


def piano_practice_difficulty_to_hard():
    global piano_window
    if piano_window:
        piano_window.set_practice_difficulty(PracticeLevel.HARD)
        pass
    pass


def piano_practice_difficulty_to_hell():
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
