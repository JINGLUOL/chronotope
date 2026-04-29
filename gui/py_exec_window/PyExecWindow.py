import os

from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QTextEdit

from pyqt.qt5.util.InputAreaDialog import InputAreaDialog


class PyExecWindow(QWidget):
    def __init__(self, parent=None):
        super(PyExecWindow, self).__init__(parent, Qt.Window)

        self.setWindowTitle('脚本执行器')

        self.process = QProcess(self)
        ''' 执行对象 '''

        self.args_input = QTextEdit()
        ''' 执行文件地址输入框 '''
        self.exec_path_input = QLineEdit()
        ''' 执行文件地址输入框 '''

        self.exec_path_btn = QPushButton('选择.PY文件位置')
        ''' 执行文件地址选择按钮 '''
        self.exec_btn = QPushButton('执行文件')
        ''' 执行文件按钮 '''
        self.file_stdout: [str] = []
        ''' 文件执行输出 '''

        self.init_ui()
        self.mount_event()
        pass

    def init_ui(self):
        layout = QVBoxLayout(self)

        args_line = QWidget(self)
        args_line_layout = QHBoxLayout(args_line)
        label = QLabel('执行参数：')
        label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        args_line_layout.addWidget(label)
        args_line_layout.addWidget(self.args_input)
        layout.addWidget(args_line)

        input_box = QWidget(self)
        input_box_layout = QHBoxLayout(input_box)
        label = QLabel('执行文件：')
        label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        input_box_layout.addWidget(label)
        input_box_layout.addWidget(self.exec_path_input)
        input_box_layout.addWidget(self.exec_path_btn)
        layout.addWidget(input_box)

        layout.addWidget(self.exec_btn)
        pass

    def mount_event(self):
        self.exec_path_input.setReadOnly(True)
        self.args_input.setAcceptRichText(False)
        self.exec_path_btn.clicked.connect(self._choose_save_path)
        self.exec_btn.clicked.connect(self._exec_file)
        self.process.readyReadStandardOutput.connect(self._exec_file_stdout)
        self.process.finished.connect(self._exec_file_result)
        pass

    def _choose_save_path(self):
        path, _ = QFileDialog.getOpenFileName(self, '选择执行文件', '', "Python 文件 (*.py)")
        if not path: return
        self.exec_path_input.setText(path)
        pass

    def _exec_file(self):
        file_path = self.exec_path_input.text()
        if not os.path.exists(file_path): return
        args = self.args_input.toPlainText().strip().split('\n')
        if args[0]:
            self.process.start("python", [file_path] + args)
        else:
            self.process.start("python", [file_path])
        pass

    def _exec_file_stdout(self):
        # 读取所有可用的输出（可能有多次触发）
        data = self.process.readAllStandardOutput()
        text = data.data().decode('utf-8', errors='ignore')
        self.file_stdout.append(text)
        pass

    def _exec_file_result(self):
        InputAreaDialog(
            '程序执行结果 ↓', self,
            '\n'.join(self.file_stdout), True
        ).exec()
        self.file_stdout.clear()
        pass

    pass
