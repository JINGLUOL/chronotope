__all__ = ['go_game_window']

from .GoGameWindow import GoGameWindow

window: GoGameWindow | None = None


def go_game_window(parent=None) -> None:
    global window
    if window is None:
        window = GoGameWindow()
        if parent: window.setWindowIcon(parent.windowIcon())
        pass
    window.toggle_visibility()
    pass
