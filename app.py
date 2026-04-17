import sys
import threading
from functools import partial

import pygame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu

from app_work import gk_work
from c_os.keyboard import GlobalKeyboardListener
from global_manager import resources, screen
from gui import *

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
pygame.init()

app_icon = QIcon(resources.icon)

menu_window = ListMenuWindow(
    screen.x, screen.y, screen.width, screen.height,
    list_width=430, list_height=670, item_height=67
)
menu_window.setWindowIcon(app_icon)
""" 应用菜单 """


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

    sprites_window = SpritesWindow(screen.x, screen.y, screen.width, screen.height)
    """ 精灵窗口 """

    """ 菜单窗口 """
    menu_window.load_data({
        '关闭菜单': menu_window.hide,
        '显示所有窗口': app_show,
        '隐藏所有窗口': app_hide,
        '工具': {
            '脚本运行器': py_exec_window,
            '二维码生成器': qr_code_window,
            '国开': {
                '复制报名材料列表': gk_work.copy_materials_list,
                '姓名加证件号后四位转证件号': gk_work.name_id4_to_card_id,
                '打印材料': gk_work.print_materials,
            },
        },
        '娱乐': {
            '桌面精灵': {
                '显示/隐藏': sprites_window.toggle_visibility,
                '添加一只小骑士': sprites_window.create_knight_sprite,
                '添加一只大黄蜂': sprites_window.create_hornet_sprite,
                '清除所有精灵': sprites_window.clear_sprites,
            },
            '钢琴': {
                '显示/隐藏': piano_window.piano_toggle_visibility,
                '琴键生成': {
                    '3个八度': partial(piano_window.create_piano, octaves=3),
                    '5个八度': partial(piano_window.create_piano, octaves=5),
                    '7个八度': partial(piano_window.create_piano, octaves=7),
                },
                '模式选择': {
                    '经典模式': partial(piano_window.set_difficulty, difficulty=piano_window.PracticeLevel.NONE),
                    '练习模式': {
                        '简单': partial(piano_window.set_difficulty, difficulty=piano_window.PracticeLevel.EASY),
                        '普通': partial(piano_window.set_difficulty, difficulty=piano_window.PracticeLevel.NORMAL),
                        '困难': partial(piano_window.set_difficulty, difficulty=piano_window.PracticeLevel.HARD),
                        '地狱': partial(piano_window.set_difficulty, difficulty=piano_window.PracticeLevel.HELL),
                    }
                },
                '关闭': piano_window.delete_piano_window,
            },
        },
        # '设置': print,
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
