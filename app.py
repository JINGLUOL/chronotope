import sys
import threading

import pygame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu

from app_work.tool_work import gk_work
from util.c_os.keyboard import GlobalKeyboardListener
from global_manager import resources, config
from gui import tool_window, ListMenuWindow
from gui.game_window import sprites_window, piano_window, go_game_window

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
app.setStyleSheet(open(resources.app_stylesheet, encoding="utf-8").read())
pygame.init()

app_icon = QIcon(resources.icon)

menu_window = ListMenuWindow(
    config.screen_root.x, config.screen_root.y,
    config.screen_root.width, config.screen_root.height,
    list_width=430, list_height=670, item_height=67
)
menu_window.setWindowIcon(app_icon)
""" 应用菜单 """


def app_reset_stylesheet():
    app.setStyleSheet(open(resources.app_stylesheet, encoding="utf-8").read())
    pass


def app_show():
    for window in app.topLevelWindows():
        if not window.isVisible():
            window.show()
            pass
        pass
    pass


def app_hide():
    for window in app.topLevelWindows():
        if window.isVisible():
            window.close()
            pass
        pass
    pass


def app_exit():
    app_hide()

    ''' 用来关闭应用的延时器 延迟半秒执行 '''
    threading.Timer(0.5, QApplication.quit).start()
    pass


if __name__ == '__main__':
    """ 菜单窗口 """
    menu_window.load_data({
        '关闭菜单': menu_window.hide,
        '显示所有窗口': app_show,
        '隐藏所有窗口': app_hide,
        '工具': {
            '脚本运行器': tool_window.py_exec_window,
            '二维码生成器': tool_window.qr_code_window,
            '视频播放器': tool_window.video_window,
            '国开': gk_work.menu_config,
        },
        '娱乐': {
            '桌面精灵': sprites_window.menu_config,
            '钢琴': piano_window.menu_config,
            '围棋': go_game_window.go_game_window
        },
        '设置': {
            '重载样式表': app_reset_stylesheet
        },
        '退出应用': app_exit,
    })

    # 创建托盘图标
    tray_icon = QSystemTrayIcon(app_icon)

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
