from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout

from lib.pyqt5_ex.component import LoadingCircle


class BlockingDialog(QDialog):
    completed_signal = pyqtSignal()
    ''' 待回调函数 '''

    def __init__(self, parent=None, tip='任务执行中'):
        super().__init__(parent)
        self.setMinimumSize(330, 100)

        # 连接关闭信号
        self.completed_signal.connect(self._completed)

        # 设置禁用关闭相关设置
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # 仅保留最小化和最大化按钮，隐藏关闭按钮
        flags = self.windowFlags()
        flags &= ~Qt.WindowCloseButtonHint  # 移除关闭按钮
        flags |= Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # 确保最小化和最大化按钮存在
        self.setWindowFlags(flags)

        self.content_label = QLabel(tip)
        self.loading_circle = LoadingCircle(parent=self)
        self.closeable = False

        # 添加标题
        self.setWindowTitle('等待窗口')
        # 初始化UI
        layout = QVBoxLayout(self)
        # 添加正文
        content_layout = QHBoxLayout(self)
        content_layout.addStretch(1)
        content_layout.addWidget(self.content_label)
        content_layout.addWidget(self.loading_circle)
        content_layout.addStretch(1)
        layout.addLayout(content_layout)
        pass

    def _completed(self):
        self.content_label.setText("任务完成")
        self.loading_circle.completed()
        self.closeable = True
        super().accept()
        pass

    def accept(self):
        self.completed_signal.emit()
        pass

    def exec_(self):
        self.loading_circle.run()
        return super().exec_()

    def keyReleaseEvent(self, event):
        event.ignore()
        pass

    def keyPressEvent(self, event):
        event.ignore()
        pass

    def closeEvent(self, event):
        if self.closeable:
            super().closeEvent(event)
        else:
            event.ignore()
        pass

    pass
