from PyQt5.QtWidgets import QWidget, QTextEdit


class MessageItem(QWidget):

    def __init__(self, parent=None):
        super(MessageItem, self).__init__(parent)
        text_area = QTextEdit(self)
        pass

    pass
