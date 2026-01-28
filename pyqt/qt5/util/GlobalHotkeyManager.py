import threading

import keyboard
from PyQt5.QtCore import QObject, pyqtSignal


class GlobalHotkeyManager(QObject):
    """全局热键管理器"""

    show_hide_signal = pyqtSignal()

    def __init__(self, hotkey_show_hide='ctrl+shift+`'):
        super().__init__()
        self.hotkey_show_hide = hotkey_show_hide
        self.is_listening = True
        self.listener_thread = None
        pass

    def start(self):
        """启动热键监听线程"""
        self.listener_thread = threading.Thread(target=self._listen_hotkeys, daemon=True)
        self.listener_thread.start()
        pass

    def _listen_hotkeys(self):
        """监听热键的函数（在独立线程中运行）"""
        try:
            # 注册热键
            keyboard.add_hotkey(self.hotkey_show_hide, self._on_show_hide_triggered)
            print(f"热键已注册: {self.hotkey_show_hide} 显示/隐藏窗口")

            # 保持线程运行
            keyboard.wait()
        except Exception as e:
            print(f"热键监听错误: {e}")
            pass
        pass

    def _on_show_hide_triggered(self):
        """热键触发时的回调"""
        if self.is_listening: self.show_hide_signal.emit()
        pass

    def stop(self):
        """停止热键监听"""
        self.is_listening = False
        keyboard.unhook_all()
        pass

    pass
