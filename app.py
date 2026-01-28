import sys

import pygame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu

from global_manager import screen, resources
from pyqt.qt5.window import TransparentWindow, SpritesWindow, PianoWindow


def tray_icon_activated(reason):
    """处理托盘图标点击事件"""
    # 双击
    if reason == QSystemTrayIcon.DoubleClick:
        # 隐藏窗口
        tray_icon.showMessage(
            "提示",
            "程序已最小化到托盘",
            QSystemTrayIcon.Information,
            2000
        )
        pass
    # 单击
    elif reason == QSystemTrayIcon.Trigger:
        # 显示窗口
        pass
    pass


if __name__ == '__main__':
    pygame.init()
    app = QApplication(sys.argv)

    window = TransparentWindow(screen.x, screen.y, screen.width, screen.height)
    """ 透明窗口 """
    window.show()

    piano_window = PianoWindow(screen.x, screen.y, screen.width, screen.height, 5)
    """ 钢琴窗口 """
    piano_window.show()

    sprites_window = SpritesWindow(screen.x, screen.y, screen.width, screen.height)
    """ 桌宠窗口 """
    sprites_window.show()

    # 创建托盘图标
    tray_icon = QSystemTrayIcon(QIcon(resources.icon))

    # 创建托盘菜单
    tray_menu = QMenu()
    # 添加菜单项
    quit_action = QAction("退出")
    quit_action.triggered.connect(QApplication.quit)
    tray_menu.addAction(quit_action)
    # menu.addSeparator()
    # ...
    # 设置托盘菜单
    tray_icon.setContextMenu(tray_menu)

    # 托盘图标点击事件
    # tray_icon.activated.connect(tray_icon_activated)

    # 显示托盘图标
    tray_icon.show()

    sys.exit(app.exec_())
