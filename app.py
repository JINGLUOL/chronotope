import sys
import threading

import pygame
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu

from work import mincraft_work, gk_work
from c_os.keyboard import GlobalKeyboardListener
from global_manager import resources, screen
from gui.event_pages import *

app = QApplication(sys.argv)
pygame.init()

menu_window = ListMenuWindow(
    screen.x, screen.y, screen.width, screen.height,
    list_width=430, list_height=670, item_height=67
)
""" 应用菜单 """


def app_hide():
    menu_window.hide()
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
        '关闭菜单': menu_window.toggle_visibility,
        '隐藏所有窗口': app_hide,
        '工具': {
            'Minecraft': {
                '配置原版风格资源包': mincraft_work.keep_original_resource_pack,
            },
            '国开': {
                '复制报名材料列表': gk_work.copy_materials_list,
                '姓名+身份证后四位转身份证号码': gk_work.name_id4_to_card_id,
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
                    '3个八度': piano_window.create_octaves3_piano,
                    '5个八度': piano_window.create_octaves5_piano,
                    '7个八度': piano_window.create_octaves7_piano,
                },
                '模式选择': {
                    '经典模式': piano_window.set_difficulty_to_none,
                    '练习模式': {
                        '简单': piano_window.set_difficulty_to_easy,
                        '普通': piano_window.set_difficulty_to_normal,
                        '困难': piano_window.set_difficulty_to_hard,
                        '地狱': piano_window.set_difficulty_to_hell,
                    }
                },
                '关闭': piano_window.delete_piano_window,
            },
        },
        # '设置': print,
        '退出应用': app_exit,
    })

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
