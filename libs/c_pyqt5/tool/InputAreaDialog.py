from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit


class InputAreaDialog(QDialog):
    def __init__(
            self, tip_content: str, parent=None,
            content: str = '', readonly: bool = False
    ):
        """
        提示对话框
        :param tip_content: 提示内容
        :param parent: 对话框父类
        """
        super(InputAreaDialog, self).__init__(parent)
        self.setWindowTitle(tip_content)
        self.setModal(True)
        layout = QVBoxLayout(self)

        tip_label = QLabel(tip_content)
        tip_label.setFont(QFont("Times", 17))
        layout.addWidget(tip_label)

        self.input_area = input_area = QTextEdit()
        self.input_area.setText(content)
        self.input_area.setReadOnly(readonly)
        layout.addWidget(input_area)

        self.ok_button = QPushButton("确认", self)
        self.cancel_button = QPushButton("取消", self)
        # 连接信号槽
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        input_area.setFocus()
        pass

    def get_input(self):
        """返回用户输入的字符串，若取消则返回空字符串"""
        if self.exec_() == QDialog.Accepted:
            return self.input_area.toPlainText()
        return ""

    pass
