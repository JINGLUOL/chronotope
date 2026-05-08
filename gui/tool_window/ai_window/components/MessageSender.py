from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QTextEdit

from app_work.tool_work.ai_window_work.api import get_models
from libs.c_pyqt5.components import DynamicComboBox


class MessageSender(QWidget):
    send_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MessageSender, self).__init__(parent)

        self.model_list = DynamicComboBox(get_models, self)
        self.message = message = QTextEdit(self)
        enter = QPushButton('发送', self)

        layout = QHBoxLayout(self)
        layout.addWidget(self.model_list, alignment=Qt.AlignTop)
        layout.addWidget(message)
        layout.addWidget(enter, alignment=Qt.AlignBottom)

        def send_message():
            content = message.toPlainText()
            if content.strip(): self.send_signal.emit(content)
            pass

        enter.clicked.connect(send_message)
        pass

    pass
