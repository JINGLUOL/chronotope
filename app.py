import atexit
import sys

import keyboard
import pygame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu

from global_manager import resources, screen
from pyqt.qt5.util import GlobalHotkeyManager
from pyqt.qt5.window import *

if __name__ == '__main__':
    pygame.init()
    app = QApplication(sys.argv)

    sprites_window = SpritesWindow(screen.x, screen.y, screen.width, screen.height)
    """ 桌宠窗口 """

    menu_window = ListMenuWindow(screen.x, screen.y, screen.width, screen.height)
    """ 菜单窗口 """
    menu_window.load_data({
        '隐藏窗口': menu_window.toggle_visibility,
        '娱乐': {
            '桌面精灵': {
                '显示/隐藏': sprites_window.toggle_visibility,
                '添加一只小骑士': sprites_window.create_knight_sprite,
                '添加一只大黄蜂': sprites_window.create_hornet_sprite
            },
            '钢琴': {
                '显示/隐藏': piano_toggle_visibility,
                '生成3个八度': create_octaves3_piano,
                '生成5个八度': create_octaves5_piano,
                '生成7个八度': create_octaves7_piano,
                '关闭': delete_piano_window,
            },
        },
        '关闭应用': QApplication.quit,
    })

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
    hotkey_manager = GlobalHotkeyManager('ctrl+`')
    hotkey_manager.show_hide_signal.connect(menu_window.toggle_visibility)
    hotkey_manager.start()
    atexit.register(keyboard.unhook_all)
    sys.exit(app.exec_())
