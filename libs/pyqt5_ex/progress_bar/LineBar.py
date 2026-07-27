from PyQt5.QtWidgets import QProgressBar


class LineBar(QProgressBar):
    def __init__(self, parent=None):
        super(LineBar, self).__init__(parent)
        self.setRange(0, 100)
        self.setValue(0)
