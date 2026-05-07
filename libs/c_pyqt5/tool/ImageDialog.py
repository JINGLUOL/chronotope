from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton


class ImageDialog(QDialog):
    def __init__(
            self,
            tip_content: str,
            img: QImage,
            parent=None
    ):
        """
        提示对话框
        :param tip_content: 提示内容
        :param img: 图一
        :param parent: 对话框父类
        """
        super(ImageDialog, self).__init__(parent)
        self.setWindowTitle(tip_content)
        self.setModal(True)
        width, height = 550, 700
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        layout = QVBoxLayout(self)

        tip_label = QLabel(tip_content)
        tip_label.setFont(QFont("Times", 17))
        layout.addWidget(tip_label)

        self.img_label = img_label = QLabel()
        self.img_label.setPixmap(QPixmap(
            img.scaled(
                int(width / 3) * 2, int(height / 3) * 2,
                Qt.KeepAspectRatio, Qt.FastTransformation
            )
        ))
        layout.addWidget(img_label)

        self.ok_button = QPushButton("确认", self)
        self.cancel_button = QPushButton("取消", self)
        # 连接信号槽
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)
        pass

    def get_result(self):
        """ 获取用户选择结果 """
        if self.exec_() == QDialog.Accepted:
            return True
        return False

    pass
