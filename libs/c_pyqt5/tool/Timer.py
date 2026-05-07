from typing import Callable

from PyQt5.QtCore import QTimer


class Timer:
    def __init__(self):
        self.interval: int = 16  # 60FPS

        self.timer = QTimer()
        self.timer.start()
        pass

    def set_interval(self, interval: int):
        self.interval = interval
        self.timer.setInterval(interval)
        pass

    def start_timer(self):
        self.timer.start()
        pass

    def stop_timer(self):
        self.timer.stop()
        pass

    def out_connect(self, callback: Callable[[], None]):
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(callback)
        pass

    def out_disconnect(self, callback: Callable[[], None]):
        try:
            self.timer.timeout.disconnect(callback)
        except Exception as e:
            print('this connect is not exists(ignored error: disconnect):', e)
        pass

    pass


timer = Timer()
