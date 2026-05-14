import threading

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QTextEdit, QComboBox, QVBoxLayout

from app_work.tool_work.ai_window_work.api import get_models


class MessageSender(QWidget):
    send_slot = pyqtSignal(str)
    reload_models_slot = pyqtSignal(list)

    def __init__(self, parent=None):
        super(MessageSender, self).__init__(parent)

        left_box = QVBoxLayout()
        self.model_list = QComboBox(self)
        reload_models_btn = QPushButton('重载模型列表', self)

        left_box.addWidget(self.model_list)
        left_box.addWidget(reload_models_btn)

        self.message = message = QTextEdit(self)

        enter_btn = QPushButton('发送', self)

        layout = QHBoxLayout(self)
        layout.addLayout(left_box)
        layout.addWidget(message)
        layout.addWidget(enter_btn, alignment=Qt.AlignBottom)

        # 重载模组列表事件绑定
        self.reload_models_thread = threading.Thread(target=self._get_models_work)
        self.reload_models_slot.connect(self.reload_models)
        reload_models_btn.clicked.connect(self.reload_models_thread.start)

        # 发送消息事件绑定
        enter_btn.clicked.connect(self._send_message)
        pass

    def _send_message(self):
        content = self.message.toPlainText()
        if content.strip(): self.send_slot.emit(content)
        pass

    def _get_models_work(self):
        self.reload_models_slot.emit(get_models())
        pass

    def reload_models(self, items: list[str]):
        self.model_list.clear()
        self.model_list.addItems(items)
        pass

    pass
