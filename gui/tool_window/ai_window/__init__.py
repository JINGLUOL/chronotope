__all__ = ['ai_window', 'window']

from .AIWindow import AIWindow

window: AIWindow | None = None


def ai_window(parent=None) -> AIWindow | None:
    global window
    if parent is None: return window
    if window is None:
        window = AIWindow()
        if parent: window.setWindowIcon(parent.windowIcon())
        pass
    window.toggle_visibility()
    pass
