import sys

import pygame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu

app = QApplication(sys.argv)
pygame.init()

from cos.keyboard import GlobalKeyboardListener
from global_manager import resources
from gui.event_pages import *

if __name__ == '__main__':
    # 创建托盘图标
    tray_icon = QSystemTrayIcon(QIcon(resources.icon))

    # 创建托盘菜单
    tray_menu = QMenu()
    # 添加菜单项
    quit_action = QAction("退出")
    quit_action.triggered.connect(app_exit)
    tray_menu.addAction(quit_action)
    # menu.addSeparator()
    # ...
    # 设置托盘菜单
    tray_icon.setContextMenu(tray_menu)


    # 托盘图标点击事件
    def tray_icon_activated(reason):
        """处理托盘图标点击事件"""
        # 单击
        if reason == QSystemTrayIcon.Trigger:
            # 显示/隐藏窗口
            menu_window.toggle_visibility()
            pass
        pass


    tray_icon.activated.connect(tray_icon_activated)
    # 显示托盘图标
    tray_icon.show()

    """启动热键监听线程"""
    g_keyboard = GlobalKeyboardListener()
    g_keyboard.start()

    g_keyboard.add_release_hotkey(['Key.ctrl_l', '<192>'], menu_window.toggle_visibility_signal.emit)

    sys.exit(app.exec_())
