from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QComboBox, QListView, QStyledItemDelegate

class ComboxItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 自定义绘制逻辑，例如设置固定高度或根据内容调整高度
        option.rect.setHeight(30)  # 设置固定高度为30px
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        # 返回自定义大小提示，这将影响行高
        return QSize(option.rect.width(), 30)  # 设置固定高度为30px

class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ComboBox, self).__init__(parent)
        self.setView(QListView())
        self.view().setItemDelegate(ComboxItemDelegate())
        self.setMinimumHeight(28)