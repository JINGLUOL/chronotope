from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QMainWindow, QWidget


class TransparentWindow(QMainWindow):

    def __init__(self, x, y, width, height):
        super().__init__()
        self._init_window()
        # 设置窗口大小和位置
        self.setGeometry(x, y, width, height)

        # 显示窗口动画
        self.show_anim = QPropertyAnimation(self, b"windowOpacity")
        self.show_anim.setEasingCurve(QEasingCurve.OutSine)
        self.show_anim.setDuration(300)
        self.show_anim.setStartValue(0.0)
        self.show_anim.setEndValue(1.0)
        self.show_anim.finished.connect(super().show)

        # 隐藏窗口动画
        self.hide_anim = QPropertyAnimation(self, b"windowOpacity")
        self.hide_anim.setEasingCurve(QEasingCurve.InSine)
        self.hide_anim.setDuration(300)
        self.hide_anim.setStartValue(1.0)
        self.hide_anim.setEndValue(0.0)
        self.hide_anim.finished.connect(super().hide)

        # 创建中央部件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        pass

    def _init_window(self):
        # 设置窗口标识
        self.setWindowFlags(
            Qt.Window |
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setAttribute(Qt.WA_NoSystemBackground)  # 禁止系统背景
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)  # 允许透明绘制
        pass

    def show_window(self):
        """显示主窗口"""
        self.show()
        self.raise_()  # 将窗口提到前面
        self.activateWindow()  # 激活窗口
        pass

    def showEvent(self, event):
        if not self.isVisible():
            self.show_anim.start()
            pass
        pass

    def closeEvent(self, a0):
        """重写关闭事件，隐藏窗口而不是关闭"""
        a0.ignore()
        self.hide_anim.start()
        pass

    pass
