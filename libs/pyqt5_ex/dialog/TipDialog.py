from functools import partial

import pyperclip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QPushButton, QLabel


class TipDialog(QDialog):
    def __init__(self, tip_content: str, tip_description=None, closeable=True, parent=None):
        """
        提示对话框
        :param tip_content: 提示内容
        :param tip_description: 提示详细描述
        :param parent: 对话框父类
        """
        super(TipDialog, self).__init__(parent)
        self.tip_content = tip_content
        self.closeable = closeable
        self.setWindowTitle('Tip')
        self.setModal(True)
        layout = QVBoxLayout(self)

        content_font = QFont("Times", 17)
        content_label = QLabel(tip_content)
        content_label.setFont(content_font)
        layout.addWidget(content_label)

        # 添加复制内容按钮
        if tip_description is not None:
            description_area = QTextEdit()
            description_area.setText(tip_description)
            description_area.setReadOnly(True)
            layout.addWidget(description_area)

            copy_btn = QPushButton('复制')
            copy_btn.clicked.connect(partial(pyperclip.copy, tip_description))
            layout.addWidget(copy_btn)
            pass

        if closeable:
            exit_btn = QPushButton('确认')
            exit_btn.clicked.connect(self.close)
            layout.addWidget(exit_btn)
        else:
            # self.setWindowFlags(Qt.FramelessWindowHint)
            # 仅保留最小化和最大化按钮，隐藏关闭按钮
            flags = self.windowFlags()
            flags &= ~Qt.WindowCloseButtonHint  # 移除关闭按钮
            flags |= Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # 确保最小化和最大化按钮存在
            self.setWindowFlags(flags)
            pass
        pass

    def keyReleaseEvent(self, event):
        # 捕获ESC键事件
        if event.key() == Qt.Key_Escape and self.closeable:
            self.accept()  # 关闭对话框
        pass

    def keyPressEvent(self, event):
        pass

    pass
