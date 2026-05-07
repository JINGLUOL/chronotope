from dataclasses import dataclass

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton


@dataclass(frozen=True)
class SettingAttrTypes:
    INPUT: str = 'input'
    SINGLE: str = 'single'
    MULTIPLE: str = 'multiple'
    pass


@dataclass
class SettingAttrGroup:
    name: str
    attrs: list[str]
    attr_type: str
    value: str
    re_str: str
    description: str
    pass


@dataclass(frozen=True)
class SettingPage:
    name: str
    attr_groups: list[SettingAttrGroup]
    description: str
    pass


class SettingDialog(QDialog):
    def __init__(
            self, tip_content: str, setting_pages: list[SettingPage], parent=None,
    ):
        """
        提示对话框
        :param tip_content: 提示内容
        :param setting_pages: 设置页面列表
        :param parent: 对话框父类
        """
        super(SettingDialog, self).__init__(parent)
        self.setWindowTitle(tip_content)
        self.setModal(True)
        self.layout = QVBoxLayout(self)
        self.init_ui()
        pass

    def init_ui(self):
        ok_button = QPushButton("应用", self)
        cancel_button = QPushButton("取消", self)
        # 连接信号槽
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(cancel_button)
        self.layout.addWidget(ok_button)
        pass

    def get_result(self):
        """返回用户输入的字符串，若取消则返回空字符串"""
        if self.exec_() == QDialog.Accepted:
            pass
        pass

    pass
