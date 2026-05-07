from screeninfo import get_monitors


class Screen:

    def __init__(self, s_id, x, y, width, height):
        self.id = s_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale: float = 1.0
        pass

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    pass


def get_screens() -> dict[int, Screen]:
    """获取多显示器中，每一个屏幕的 缩放前原始物理分辨率"""
    monitor_list = get_monitors()
    screens = {}
    for idx, monitor in enumerate(monitor_list):
        screen = Screen(
            idx + 1,
            monitor.x, monitor.y,
            monitor.width, monitor.height,
        )
        screens[screen.id] = screen
        pass
    return screens
