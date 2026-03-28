__all__ = [
    'menu_window',
    'app_hide',
    'app_exit'
]

import threading

from PyQt5.QtWidgets import QApplication

from global_manager import screen
from work import gk_work, mincraft_work
from .ListMenuWindow import ListMenuWindow
from ..sprites_window import *

menu_window = ListMenuWindow(
    screen.x, screen.y, screen.width, screen.height,
    list_width=430, list_height=670, item_height=67
)
sprites_window = SpritesWindow(screen.x, screen.y, screen.width, screen.height)
""" 应用菜单 """


def app_hide():
    menu_window.hide()
    sprites_window.hide()
    pass


def app_exit():
    app_hide()

    ''' 用来关闭应用的延时器 延迟半秒执行 '''
    threading.Timer(0.5, QApplication.quit).start()
    pass


""" 菜单窗口 """
menu_window.load_data({
    '关闭菜单': menu_window.toggle_visibility,
    '隐藏所有窗口': app_hide,
    '工具': {
        'Minecraft': {
            '配置为原版风格资源包': mincraft_work.keep_original_resource_pack(),
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
    },
    # '设置': print,
    '退出应用': app_exit,
})
