__all__ = ['config', 'resources', 'log']

import atexit
import os
import sys
import threading
import traceback
from collections import deque
from datetime import datetime
from typing import Any

from pynput import mouse

from util.c_os.screen import get_screens, Screen


class Config:

    def __init__(self):
        # 线程锁
        self.lock = threading.Lock()

        # 日志缓存
        self._logs: deque[Any] = deque(maxlen=3000)
        self.has_error = False

        # 添加程序结束回调
        atexit.register(self._write_log)

        # 添加主线程异常钩子
        sys.excepthook = self._global_exception_handler

        # 添加辅线程异常钩子
        threading.excepthook = self._global_thread_exception_handler

        # 监听鼠标移动
        self.mouse_x = 0
        self.mouse_y = 0
        self._mouse_handler()

        self.screens: dict[int, Screen] = get_screens()
        self.screen_root: Screen = self.screens[1]
        pass

    def _mouse_handler(self) -> None:
        def mouse_move_work(x: int, y: int):
            self.mouse_x = x
            self.mouse_y = y
            pass
        threading.Thread(
            target=mouse.Listener(on_move=mouse_move_work).start,
            daemon=True,
        ).start()
        pass

    def _global_thread_exception_handler(self, args: Any) -> None:
        self._global_exception_handler(args.exc_type, args.exc_value, args.exc_traceback)
        pass

    def _global_exception_handler(self, exc_type, exc_value, exc_traceback):
        """
        全局异常处理函数
        """

        # 忽略 KeyboardInterrupt（Ctrl+C）异常
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.has_error = True
        error_msg = \
            f"""
╔═══════════════════════════════════════════════════════════╗
║                    全局异常捕获报告                          ║
╚═══════════════════════════════════════════════════════════╝
异常类型: {exc_type.__name__}
异常信息: {exc_value}

异常追踪:
{''.join(traceback.format_tb(exc_traceback))}
"""
        self.cache_log(error_msg)
        pass

    def _write_log(self):
        self.cache_log('program exit', write=True)
        pass

    def cache_log(
            self, *content: Any, sep: str = ' ', end: str = '\n',
            write: bool = False
    ):
        now = datetime.now()
        time_str = f"{now.hour:02d}_{now.minute:02d}_{now.second:02d}.{(now.microsecond//1000):03d}"
        content = f"{time_str} ---> {sep.join([str(ctt) for ctt in content])}"
        print(content)
        self._logs.append(content)

        if write and self.has_error:
            with self.lock:
                output_path = resources.output_log(
                    f'program log---{time_str}',
                    f"\\{now.strftime('%Y_%m_%d')}",
                )
                open(output_path, encoding="utf-8", mode="w").write(end.join(self._logs))
                self._logs.clear()
                pass
            pass

        pass

    def get_focus_screen(self) -> Screen:
        for screen in self.screens.values():
            if screen.is_include(self.mouse_x, self.mouse_y):
                return screen
        return self.screen_root

    pass


config: Config = Config()


def log(*message: Any) -> None:
    config.cache_log(*message)
    pass


def exe_path(relative_path: str | None = None, to_resources: bool = False):
    """ 精准找到执行文件的绝对路径 """

    # 检查是否是打包后的exe环境
    if getattr(sys, 'frozen', False):
        # 如果是PyInstaller打包的exe，使用_MEIPASS或exe所在目录
        # getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        if relative_path is None:
            return os.path.dirname(sys.executable)
        elif to_resources:
            return f"{os.path.dirname(sys.executable)}\\_internal\\{relative_path}"
        else:
            return f"{os.path.dirname(sys.executable)}\\{relative_path}"
    else:
        # 开发环境下使用脚本所在目录
        return f"{os.path.dirname(os.path.abspath(__file__))}\\{relative_path}"


class Resource:

    def __init__(self):
        self.icon = exe_path('resources\\icon.ico', True)

        self.user_folder = exe_path('JINGLUO_app_cache\\user')

        self.log_folder = exe_path('JINGLUO_app_cache\\log')

        self.data_folder = exe_path('JINGLUO_app_cache\\data')

        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        self.app_stylesheet = exe_path('resources\\App_StyleSheets\\default_stylesheet.qss', True)
        self.Knight = exe_path('resources\\Sprites\\HollowKnight\\Knight', True)
        self.Hornet = exe_path('resources\\Sprites\\HollowKnight\\Hornet', True)
        self.SumatraPDF = exe_path('resources\\SumatraPDF\\SumatraPDF-3.6-64.exe', True)
        self.VoskSmallCNModel = exe_path('resources\\AudioRecognizerBase\\vosk-model-small-cn-0.22', True)
        pass

    def output_log(self, filename: str, subfolder: str = None):
        if subfolder:
            folder_path = f"{self.log_folder}\\{subfolder}"
            if not os.path.exists(folder_path): os.makedirs(folder_path)
            return f"{folder_path}\\{filename}.txt"
        else:
            return f"{self.log_folder}\\{filename}.txt"

    def output_data(self, filename: str, subfolder: str = None):
        if subfolder:
            folder_path = f"{self.data_folder}\\{subfolder}"
            if not os.path.exists(folder_path): os.makedirs(folder_path)
            return f"{folder_path}\\{filename}"
        else:
            return f"{self.data_folder}\\{filename}"

    pass


resources: Resource = Resource()
