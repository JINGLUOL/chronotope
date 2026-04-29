from functools import partial

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
    piano_window.show()
    return piano_window


def create_piano(parent: TransparentWindow, octaves: int = 3) -> PianoWindow:
    return create_piano_window(parent, octaves)


def set_difficulty(parent: TransparentWindow, difficulty: PracticeLevel = PracticeLevel.NONE) -> None:
    create_piano(parent).set_practice_difficulty(difficulty)
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


menu_config = {
    '显示/隐藏': piano_toggle_visibility,
    '琴键生成': {
        '3个八度': partial(create_piano, octaves=3),
        '5个八度': partial(create_piano, octaves=5),
        '7个八度': partial(create_piano, octaves=7),
    },
    '模式选择': {
        '经典模式': partial(set_difficulty, difficulty=PracticeLevel.NONE),
        '练习模式': {
            '简单': partial(set_difficulty, difficulty=PracticeLevel.EASY),
            '普通': partial(set_difficulty, difficulty=PracticeLevel.NORMAL),
            '困难': partial(set_difficulty, difficulty=PracticeLevel.HARD),
            '地狱': partial(set_difficulty, difficulty=PracticeLevel.HELL),
        }
    },
    '关闭': delete_piano_window,
}
