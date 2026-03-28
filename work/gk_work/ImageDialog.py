from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton

from util.file.image import pil_to_qt_img, resize_fit


class ImageDialog(QDialog):
    def __init__(
            self,
            tip_content: str,
            overlay_top: Image,
            overlay_bottom: Image,
            parent=None
    ):
        """
        提示对话框
        :param tip_content: 提示内容
        :param overlay_top: 图一
        :param overlay_bottom: 图二
        :param parent: 对话框父类
        """
        super(ImageDialog, self).__init__(parent)
        self.setMinimumSize(550, 700)
        self.setMaximumSize(550, 700)
        self.overlay_top: Image.Image = overlay_top
        self.overlay_bottom: Image.Image = overlay_bottom
        self.setWindowTitle(tip_content)
        self.setModal(True)
        layout = QVBoxLayout(self)

        tip_label = QLabel(tip_content)
        tip_label.setFont(QFont("Times", 17))
        layout.addWidget(tip_label)

        self.img_label = img_label = QLabel()
        layout.addWidget(img_label)

        self.ok_button = QPushButton("确认", self)
        self.cancel_button = QPushButton("取消", self)
        # 连接信号槽
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.update_img()
        pass

    def update_img(self):
        self.img_label.setPixmap(QPixmap.fromImage(
            self.merge_img(int(self.width() / 2), int(self.height() / 2))
        ))

    def merge_img(self, width: int, height: int):
        top_x, top_y = int(width * 0.03), int(height * 0.055)
        overlay_top_w, overlay_top_h = int(width * 0.95), int(height * 0.3)
        overlay_bottom_w, overlay_bottom_h = int(width * 0.95), int(height * 0.55)

        img = Image.new('RGB', (width, height), color=(255, 255, 255))  # 白色背景
        img.paste(
            resize_fit(self.overlay_top, overlay_top_w, overlay_top_h),
            (top_x, top_y)
        )
        img.paste(
            resize_fit(self.overlay_bottom, overlay_bottom_w, overlay_bottom_h),
            (top_x, top_y + overlay_top_h + int(height * 0.015))
        )
        return pil_to_qt_img(img)

    def get_result(self):
        """ 获取用户选择结果 """
        if self.exec_() == QDialog.Accepted:
            width = 4961  # 或 4960
            height = 7016  # 或 7015
            return self.merge_img(width, height)
        return None

    def keyReleaseEvent(self, a0):
        key = a0.key()
        if key == Qt.Key_Up:
            self.overlay_top = self.overlay_top.rotate(
                90,
                expand=True,
                resample=Image.Resampling.BICUBIC,
                fillcolor=(255, 255, 255)
            )
            self.update_img()
            pass
        elif key == Qt.Key_Down:
            self.overlay_bottom = self.overlay_bottom.rotate(
                90,
                expand=True,
                resample=Image.Resampling.BICUBIC,
                fillcolor=(255, 255, 255)
            )
            self.update_img()
            pass
        pass

    pass
