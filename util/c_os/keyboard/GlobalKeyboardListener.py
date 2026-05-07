import atexit
import threading
from collections.abc import Callable
from typing import Any

from pynput import keyboard

from global_manager import log


class GlobalKeyboardListener:

    def __init__(self):
        self.listener = None
        self.press_hotkeys = {}
        self.release_hotkeys = {}
        self.pressed_keys = set()

        atexit.register(self.stop)
        pass

    def on_press(self, key):
        if key is keyboard.Key.cmd: return
        try:
            key_char = key.char
            if key_char is None: key_char = str(key)
        except AttributeError:
            key_char = str(key)
            pass
        # print(f"当前按下的键: {key_char}")
        # print(f"当前按下的键组: {self.pressed_keys}")

        # 添加按下的键
        self.pressed_keys.add(key_char)

        # 检测组合键
        self.check_press_hotkeys()
        pass

    def on_release(self, key):
        if key is keyboard.Key.cmd: return
        try:
            key_char = key.char
            if key_char is None: key_char = str(key)
        except AttributeError:
            key_char = str(key)
            pass
        # print(f"释放: {key_char}")

        # 检测组合键
        self.check_release_hotkeys()

        # 释放按下的键
        if key_char in self.pressed_keys:
            self.pressed_keys.remove(key_char)
        else:
            self.pressed_keys.clear()
            pass
        pass

    def add_press_hotkey(self, keys: list[str], callback: Callable[[], Any]):
        """注册按下时的热键"""
        self.press_hotkeys[frozenset(keys)] = callback
        pass

    def remove_press_hotkey(self, keys: list[str]):
        keys = frozenset(keys)
        if keys in self.press_hotkeys:
            self.press_hotkeys.pop(keys)
            pass
        pass

    def add_release_hotkey(self, keys: list[str], callback: Callable[[], Any]):
        """注册释放时的热键"""
        self.release_hotkeys[frozenset(keys)] = callback
        pass

    def remove_release_hotkey(self, keys: list[str]):
        keys = frozenset(keys)
        if keys in self.release_hotkeys:
            self.release_hotkeys.pop(keys)
            pass
        pass

    def check_press_hotkeys(self):
        """检查热键是否被触发"""
        current_keys = frozenset(self.pressed_keys)
        for key_combo, callback in self.press_hotkeys.items():
            if key_combo == current_keys: callback()
            pass
        pass

    def check_release_hotkeys(self):
        """检查热键是否被触发"""
        current_keys = frozenset(self.pressed_keys)
        for key_combo, callback in self.release_hotkeys.items():
            if key_combo == current_keys: callback()
            pass
        pass

    def start(self):
        """开始监听"""
        if self.listener: return

        def work():
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            self.listener.start()

        threading.Thread(target=work, daemon=True).start()
        log("键盘监听已启动")
        pass

    def stop(self):
        """停止监听"""
        if self.listener: self.listener.stop()
        log("键盘监听已停止")

    pass
