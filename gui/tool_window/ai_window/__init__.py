__all__ = ['ai_window', 'window']

from .AIWindow import AIWindow

window: AIWindow | None = None


def ai_window() -> AIWindow | None:
    global window
    if window is None:
        window = AIWindow()
        pass
    window.toggle_visibility()
    pass
