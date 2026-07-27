from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout

from pyqt5_extension.thread import WorkerThread


class ProgressDialog(QDialog):
    """自动关闭对话框"""

    def __init__(self, worker_thread: WorkerThread, parent=None):
        super().__init__(parent)
        self.setWindowTitle("处理中...")
        self.setFixedSize(300, 150)
        self.setWindowModality(Qt.ApplicationModal)  # 模态对话框

        # 创建UI组件
        self.label = QLabel("正在处理，请稍候...", self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # 禁用关闭
        flags = self.windowFlags()
        flags &= ~Qt.WindowCloseButtonHint  # 移除关闭按钮
        flags |= Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # 确保最小化和最大化按钮存在
        self.setWindowFlags(flags)

        # 创建并启动工作线程
        self.worker_thread = worker_thread
        # 连接信号与槽
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.finished.connect(self.on_finished)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)  # 清理线程
        self.worker_thread.start()
        self.exec_()

    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        if value == 100:
            self.label.setText("处理完成，即将关闭...")

    def on_finished(self):
        """线程完成后关闭对话框"""
        self.accept()  # 关闭对话框

    def keyReleaseEvent(self, event):
        pass

    def keyPressEvent(self, event):
        pass