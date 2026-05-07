from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from ..components import CWidget


class TransparentWindow(QMainWindow):

    def __init__(self, x: int, y: int, width: int, height: int, full_op: bool = True):
        super().__init__()
        # 设置窗口标识
        self.setWindowFlags(
            Qt.Window |
            Qt.Tool |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        # 设置窗口背景透明
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)  # 允许透明绘制
        if full_op:
            self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
            self.setAttribute(Qt.WA_NoSystemBackground)  # 禁止系统背景
        # 设置窗口大小和位置
        self.setGeometry(x, y, width, height)

        # 显示窗口动画
        self.show_anim = QPropertyAnimation(self, b"windowOpacity")
        self.show_anim.setEasingCurve(QEasingCurve.OutSine)
        self.show_anim.setDuration(300)
        self.show_anim.setStartValue(0.0)
        self.show_anim.setEndValue(1.0)
        self.show_anim.finished.connect(self.activate_window)

        # 隐藏窗口动画
        self.hide_anim = QPropertyAnimation(self, b"windowOpacity")
        self.hide_anim.setEasingCurve(QEasingCurve.InSine)
        self.hide_anim.setDuration(300)
        self.hide_anim.setStartValue(1.0)
        self.hide_anim.setEndValue(0.0)
        self.hide_anim.finished.connect(super().hide)

        # 关闭窗口动画
        self.close_anim = QPropertyAnimation(self, b"windowOpacity")
        self.close_anim.setEasingCurve(QEasingCurve.InSine)
        self.close_anim.setDuration(300)
        self.close_anim.setStartValue(1.0)
        self.close_anim.setEndValue(0.0)
        self.close_anim.finished.connect(super().destroy)

        # 创建中央部件
        self.central_widget = CWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        pass

    @classmethod
    def from_widget(cls, widget: QWidget, full_op: bool = True):
        return cls(widget.x(), widget.y(), widget.width(), widget.height(), full_op)

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            pass
        pass

    def activate_window(self):
        self.raise_()  # 将窗口提到前面
        self.activateWindow()  # 激活窗口
        pass

    def showEvent(self, event):
        self.show_anim.start()
        super().showEvent(event)
        pass

    def hide(self):
        self.hide_anim.start()
        pass

    def closeEvent(self, a0):
        a0.ignore()
        self.hide_anim.start()
        pass

    def destroy(self, d_win=..., d_sub_wins=...):
        self.close_anim.start()
        pass

    pass
