from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class DebouncedLineEdit(QLineEdit):
    stopTyping = pyqtSignal(str)
    ''' 停止输入的延迟信号槽 '''

    def __init__(self, contents: str, parent=None, delay=370):
        super().__init__(contents, parent)
        self.delay = delay
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_stop_typing)
        # 监听文本变化信号（或者 textEdited 区别程序修改）
        self.textChanged.connect(self._on_text_changed)
        pass

    def _on_text_changed(self, text):
        """每次文本改变时，重置定时器"""
        self._timer.stop()
        self._timer.start(self.delay)
        pass

    def _on_stop_typing(self):
        """用户停止输入后触发，发出自定义信号"""
        self.stopTyping.emit(self.text())  # 发射自定义信号
        pass

    pass
