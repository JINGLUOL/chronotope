from global_manager import screen
from .PianoWindow import PianoWindow

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


def delete_piano_window():
    global piano_window
    if piano_window:
        piano_window.destroy()
        piano_window = None
        pass
    pass
