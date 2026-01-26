from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSystemTrayIcon, QAction, QMenu, QApplication, QWidget

from global_manager import resources


class TransparentWindow(QMainWindow):

    def __init__(self, x, y, width, height):
        super().__init__()

        # 设置窗口标识
        self.setWindowFlags(
            Qt.Window |
            Qt.FramelessWindowHint |
            Qt.Tool
        )

        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置窗口大小和位置
        self.setGeometry(x, y, width, height)

        # 创建中央部件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 设置布局
        self.layout = QVBoxLayout(self.central_widget)

        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self._init_tray_icon()
        pass

    def _init_tray_icon(self):
        # 设置托盘图标（可以使用自定义图标）
        self.tray_icon.setIcon(QIcon(resources.icon))

        # 创建托盘菜单
        tray_menu = QMenu()

        # 添加菜单项
        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)

        # 托盘图标点击事件
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 显示托盘图标
        self.tray_icon.show()
        pass

    def tray_icon_activated(self, reason):
        """处理托盘图标点击事件"""
        # 双击
        if reason == QSystemTrayIcon.DoubleClick:
            self.hide_to_tray()
            pass
        # 单击
        elif reason == QSystemTrayIcon.Trigger:
            self.show_window()
            pass
        pass

    def show_window(self):
        """显示主窗口"""
        self.show()
        self.raise_()  # 将窗口提到前面
        self.activateWindow()  # 激活窗口

    def hide_to_tray(self):
        """隐藏到托盘"""
        self.hide()

    def quit_application(self):
        """退出应用程序"""
        self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event):
        """重写关闭事件，隐藏窗口而不是关闭"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "提示",
            "程序已最小化到托盘",
            QSystemTrayIcon.Information,
            2000
        )

    pass
