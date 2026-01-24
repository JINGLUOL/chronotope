from screeninfo import get_monitors


class Screen:

    def __init__(self, s_id, width, height, position):
        self.id = s_id
        self.width = width
        self.height = height
        self.position = position
        self.scale: float = 1.0
        pass

    pass


def get_screens() -> dict[int, Screen]:
    """获取多显示器中，每一个屏幕的 缩放前原始物理分辨率"""
    monitor_list = get_monitors()
    screens = {}
    for idx, monitor in enumerate(monitor_list):
        screen = Screen(
            idx + 1,
            monitor.width, monitor.height,
            (monitor.x, monitor.y)
        )
        screens[screen.id] = screen
        pass
    return screens
