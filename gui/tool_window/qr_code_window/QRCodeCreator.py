from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget, QLineEdit, QPushButton, \
    QFileDialog
from pyqtgraph import ComboBox

from util.file.image.qr_code import create_qr_code


class QRCodeCreator(QWidget):
    def __init__(self, parent=None):
        super(QRCodeCreator, self).__init__(parent, Qt.Window)
        self.setWindowTitle('二维码生成器')

        self.page_controller = QStackedWidget()
        ''' 页面控制器 '''

        self.page_title = QLabel('二维码生成器')
        ''' 页面标题 '''
        self.save_path_input = QLineEdit()
        ''' 保存地址输入框 '''
        self.save_path_btn = QPushButton('选择保存位置')
        ''' 保存地址按钮 '''
        self.content_input = QLineEdit()
        ''' 二维码内容输入框 '''
        self.create_button = QPushButton('Create QR Code')
        ''' 二维码生成按钮 '''
        self.model_list = ComboBox()
        ''' 二维码生成模式 '''

        self.init_ui()
        self.mount_event()
        pass

    def init_ui(self):
        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        body = QHBoxLayout()
        footer = QHBoxLayout()

        layout.addLayout(header)
        layout.addLayout(body)
        layout.addLayout(footer)

        """ Header """
        header.addWidget(self.page_title)

        """ Body """
        ''' Body Left '''
        body_left_widget = QWidget(self)
        body_left_widget.setProperty('class', 'card')
        body_left = QVBoxLayout(body_left_widget)

        bl_top1 = QVBoxLayout()
        label = QLabel('二维码内容：')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        bl_top1.addWidget(label)
        label = QLabel('保存位置：')
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        bl_top1.addWidget(label)
        bl_top2 = QVBoxLayout()
        bl_top2.addWidget(self.content_input)
        bl_top2.addWidget(self.save_path_input)
        bl_top3 = QVBoxLayout()
        bl_top3.addWidget(QLabel(''))
        bl_top3.addWidget(self.save_path_btn)
        bl_top = QHBoxLayout()
        bl_top.addLayout(bl_top1)
        bl_top.addLayout(bl_top2)
        bl_top.addLayout(bl_top3)
        body_left.addLayout(bl_top)
        page_controller = self.page_controller
        body_left.addWidget(self.page_controller)

        ''' 子页面一 '''
        void_page = QWidget()
        void_page_layout = QVBoxLayout(void_page)
        void_page.setProperty('class', 'card')
        label = QLabel('模式：快速生成模式')
        void_page_layout.addWidget(label)
        page_controller.addWidget(void_page)

        ''' 子页面二 '''
        config_page = QWidget()
        config_layout = QVBoxLayout(config_page)
        config_page.setProperty('class', 'card')
        label = QLabel('模式：高级生成模式')
        config_layout.addWidget(label)
        page_controller.addWidget(config_page)

        body.addWidget(body_left_widget)
        ''' Body Right '''
        body_right_widget = QWidget()
        body_right_widget.setProperty('class', 'card')
        body_right = QVBoxLayout(body_right_widget)
        body_right.setAlignment(Qt.AlignTop)

        model_list = self.model_list
        model_list.currentIndexChanged.connect(self.switch_child_page)
        model_list.addItems(('快速生成模式', '高级生成模式'))
        body_right.addWidget(model_list)

        body_right.addWidget(self.create_button)
        body.addWidget(body_right_widget)

        """ Footer """
        pass

    def switch_child_page(self, index):
        self.page_controller.setCurrentIndex(index)
        pass

    def mount_event(self):
        self.create_button.clicked.connect(self._create_qr_code)
        self.save_path_input.setReadOnly(True)
        self.save_path_btn.clicked.connect(self._choose_save_path)
        pass

    def _create_qr_code(self):
        create_qr_code(
            self.content_input.text(),
            self.save_path_input.text()
        )

    def _choose_save_path(self):
        path = QFileDialog.getExistingDirectory(self, '选择输出文件夹', '', QFileDialog.ShowDirsOnly)
        if not path: return
        self.save_path_input.setText(path)
        pass

    pass
