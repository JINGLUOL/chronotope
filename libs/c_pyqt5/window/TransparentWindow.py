from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

import global_manager


class TransparentWindow(QMainWindow):

    def __init__(self, auto_screen_size=True):
        super().__init__()

        self.auto_screen_size = auto_screen_size
        ''' 自动为当前屏幕大小显示 '''

        # 设置窗口标识
        self.setWindowFlags(
            Qt.Window |
            Qt.Tool |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        # 设置窗口背景透明
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)  # 允许透明绘制
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setAttribute(Qt.WA_NoSystemBackground)  # 禁止系统背景

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
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("TWC")
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        pass

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

    def show(self):
        # 设置窗口大小和位置
        screen_geometry = global_manager.config.get_focus_screen().get_geometry()
        if self.auto_screen_size:
            self.setGeometry(*screen_geometry)
            pass
        else:
            self.setGeometry(
                int((screen_geometry[0] + screen_geometry[2] - self.width()) / 2),
                int((screen_geometry[1] + screen_geometry[3] - self.height()) / 2),
                self.width(), self.height()
            )
            pass
        super().show()
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

    def keyReleaseEvent(self, a0):
        key = a0.key()
        if key == Qt.Key_Escape:
            self.hide()
            pass
        pass

    pass
