from typing import Callable, Any

from global_manager import config
from pyqt.qt5.components.list_menu import *
from pyqt.qt5.components.list_menu import ItemList
from .base import TransparentWindow


class ListMenuWindow(TransparentWindow):

    def __init__(
            self,
            x: int, y: int, w: int, h: int,
            data: dict[str, Callable[[], None] | Any] | None = None,
            list_width: int = 433, list_height: int = 707,
            item_height: int = 77,
    ):
        super(ListMenuWindow, self).__init__(x, y, w, h)

        self.setStyleSheet("""
        ItemList {
            background-color: transparent;
            border: none;
        }
        ItemList::item {
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 211),
                stop:0 rgba(179, 217, 240 255),
                stop:1 rgba(179, 217, 240, 255),
                stop:1 rgba(215, 238, 248, 211)
            );
            font-size: 32px;
            font-weight: 900;
            margin-top: 3px;
            padding-left: 10px;
            border-radius: 7px;
        }
        ItemList::item:hover {
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(0, 0, 0, 170),
                stop:0 rgba(183, 110, 121, 255),
                stop:1 rgba(183, 110, 121, 255),
                stop:1 rgba(0, 0, 0, 170)
            );
            color: rgb(255, 255, 255);
        }
        """)

        self.mouse_y: int = 0

        # 组件参数
        self.item_height = item_height

        # 列表宽高
        self.list_width = list_width
        self.list_height = list_height

        # 组件事件映射表
        self.item_event_map = {}

        # 上一个显示的列表
        self.pre_item_list_map: dict[int, ItemList] = {}

        # 初始化菜单
        self.root_list = None
        if data: self.load_data(data)
        pass

    def _load_data(
            self,
            data: dict[str, Callable[[], None] | Any],
            depth: int = 1,
    ) -> ItemList:
        item_list = ItemList(self.central_widget, self.list_width, self.list_height, depth)
        item_list.setItemDelegate(ItemsDelegate(self.item_height))
        # 列表内 item 事件
        item_list.itemClicked.connect(self.clicked_item_handle)
        item_list.setMouseTracking(True)
        item_list.itemEntered.connect(self.hover_item_handle)
        for item_text in data:
            # 如果仍是字典进行递归
            if isinstance(data[item_text], dict):
                list_item = ItemListItem(
                    f"↓↓ {item_text}", depth,
                    self._load_data(data[item_text], depth + 1),
                )
                pass
            # 注册事件
            else:
                list_item = ItemListItem(item_text, depth)
                self.item_event_map[item_text] = data[item_text]
                pass
            item_list.addItem(list_item)
            pass
        return item_list

    def load_data(self, data: dict[str, Callable[[], None] | Any]) -> None:
        self.root_list = self._load_data(data)
        self.root_list.setGeometry(0, 0, self.list_width, self.list_height)
        self.root_list.show()
        pass

    def clicked_item_handle(self, item: ItemListItem):
        if not item.item_list:
            self.item_event_map[item.text()]()
            pass
        pass

    def hover_item_handle(self, item: ItemListItem):
        if item.item_list:
            item_list = item.item_list
            item_depth = item.item_depth

            # 隐藏低层级的显示列表
            for i_list in self.pre_item_list_map.values():
                if i_list.item_depth > item_depth:
                    i_list.hide()
                pass
            self.pre_item_list_map[item_depth] = item_list
            x = self.root_list.x() + (self.list_width + 3) * item_depth
            y = self.root_list.y() + self.item_height * item_depth
            item_list.move(x, y)
            item_list.show()
            pass
        else:
            for i_list in self.pre_item_list_map.values():
                if i_list.item_depth > item.item_depth:
                    i_list.hide()
                pass
        pass

    def show(self):
        self.root_list.move(config.mouse_x, config.mouse_y)
        super().show()
        pass

    def hide(self):
        for i_list in self.pre_item_list_map.values():
            i_list.hide()
        self.pre_item_list_map.clear()
        super().hide()

    pass
