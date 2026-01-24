import threading
from abc import abstractmethod

import pystray
from PIL import Image

from cos.keyboard import GlobalKeyboardListener
from global_manager import resources


class Window:

    def __init__(self, width, height):
        """ 窗口参数初始化 """
        self.width = width
        self.height = height

        self.tray_icon = self.init_tray()
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

        self.running = True
        """ 程序进程控制 """
        self.hidden = False
        """ 窗口隐藏 """

        # 全局键盘监听
        self.key_listener = GlobalKeyboardListener()
        # 注册热键
        self.key_listener.add_release_hotkey(['Key.ctrl_l', '<192>'], self.toggle_hidden)
        self.key_listener.start()
        pass

    @abstractmethod
    def get_focus(self):
        """ 窗口获取焦点 """
        pass

    def toggle_hidden(self, icon=None, item=None):
        """ 切换窗口隐藏 """
        self.hidden = not self.hidden
        if not self.hidden: self.get_focus()
        pass

    def quit_app(self, icon=None, item=None):
        """ 退出应用 """
        self.running = False
        pass

    def init_tray(self):
        """ 初始化托盘 """
        image = Image.open(resources.icon)

        # 创建托盘菜单
        menu = pystray.Menu(
            pystray.MenuItem('切换显示', self.toggle_hidden),
            pystray.MenuItem('退出', self.quit_app)
        )

        # 创建托盘图标
        tray_icon = pystray.Icon("pygame_app", image, "Pygame应用", menu)

        return tray_icon

    @abstractmethod
    def run(self):
        """ 运行窗口 """
        pass

    pass
