from PyGameWindow import PyGameWindow
from global_manager import config

if __name__ == '__main__':
    # 获取主屏幕
    root = config.screen_root

    window = PyGameWindow(root.width, root.height)
    window.run()
    pass
