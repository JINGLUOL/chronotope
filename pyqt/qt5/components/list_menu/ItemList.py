from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QStyledItemDelegate, QAbstractItemView


class ItemsDelegate(QStyledItemDelegate):

    def __init__(self, height: int):
        super().__init__()
        self.height = height
        pass

    def sizeHint(self, option, index):
        # 获取默认大小
        size = super().sizeHint(option, index)
        # 设置固定高度
        size.setHeight(self.height)  # 所有项高度为60像素
        return size

    pass


class ItemList(QListWidget):

    def __init__(self, parent, width: int, height: int, item_depth: int):
        super().__init__(parent)
        self.hide()
        # 禁用选择
        self.setSelectionMode(QAbstractItemView.NoSelection)
        # 无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 关闭滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setGeometry(0, 0, width, height)
        self.item_depth = item_depth
        pass

    pass


class ItemListItem(QListWidgetItem):

    def __init__(self, text: str, item_depth: int, item_list: ItemList = None):
        super().__init__(text)

        self.item_depth: int = item_depth
        """ 组件相对于根目录的深度 """
        self.item_list = item_list
        pass

    pass
