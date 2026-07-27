from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget

_ITEM_INDEX_ATTR_NAME = 'custom_item_index'


class SimpleTreeWidget(QTreeWidget):
    item_clicked_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setHeaderHidden(True)
        self.itemClicked.connect(self._on_item_clicked)
        pass

    def _on_item_clicked(self, item, column):
        """槽函数，处理节点点击"""
        if hasattr(item, _ITEM_INDEX_ATTR_NAME):
            self.item_clicked_signal.emit(getattr(item, _ITEM_INDEX_ATTR_NAME))
            pass
        pass

    def _load_data(
            self,
            r: QTreeWidgetItem,
            data: dict[str, int | dict[str, int]]
    ):
        roots = []
        for k, v in data.items():
            root = QTreeWidgetItem(r)
            root.setText(0, k)
            roots.append(root)
            if type(v) is dict:
                root.addChildren(self._load_data(root, v))
            else:
                setattr(root, _ITEM_INDEX_ATTR_NAME, v)
        return roots

    def load_data(
            self,
            data: dict[str, int | dict[str, int]]
    ):
        for k, v in data.items():
            root = QTreeWidgetItem(self)
            root.setText(0, k)
            if type(v) is dict:
                root.addChildren(self._load_data(root, v))
            else:
                setattr(root, _ITEM_INDEX_ATTR_NAME, v)
            pass
        pass

    pass
