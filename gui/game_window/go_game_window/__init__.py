__all__ = ['go_game_window']

from .GoGameWindow import GoGameWindow

window: GoGameWindow | None = None


def go_game_window() -> None:
    global window
    if window is None: window = GoGameWindow()
    window.toggle_visibility()
    pass
