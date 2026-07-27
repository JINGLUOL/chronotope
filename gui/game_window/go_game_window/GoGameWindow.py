from libs.c_pyqt5.window import TransparentWindow
from .GoGameWidget import GoGameWidget


class GoGameWindow(TransparentWindow):

    def __init__(self):
        super().__init__(False)

        go_widget = GoGameWidget(self)
        self.setGeometry(0, 0, go_widget.board_size, go_widget.board_size)
        self.layout.addWidget(go_widget, 1)
        pass

    pass
