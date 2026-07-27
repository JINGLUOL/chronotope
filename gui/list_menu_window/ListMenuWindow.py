from typing import Callable, Any

from PyQt5 import QtCore

from global_manager import config
from libs.c_pyqt5.window import TransparentWindow
from .list_menu import *


class ListMenuWindow(TransparentWindow):
    toggle_visibility_signal = QtCore.pyqtSignal()

    def __init__(
            self,
            data: dict[str, Callable[[], None] | Any] | None = None,
            list_width: int = 433, list_height: int = 707,
            item_height: int = 77,
    ):
        super(ListMenuWindow, self).__init__()
        self.toggle_visibility_signal.connect(self.toggle_visibility)

        self.item_height = item_height
        ''' 列表项高度 '''

        # 定义列表宽高
        self.list_width = list_width
        self.list_height = list_height

        self.item_event_map = {}
        ''' 列表项事件映射表 '''

        self.pre_item_list_map: dict[int, ListMenuItem] = {}
        ''' 已显示列表深度映射表 '''

        self.root_list: ListMenuItem | None = None
        ''' 主菜单 '''
        if data: self.load_data(data)

        self.is_locked: bool = False
        ''' 菜单锁定 '''
        pass

    def _load_data(
            self,
            data: dict[str, Callable[[], None] | Any],
            abs_path: str = '',
            depth: int = 1,
    ) -> ListMenuItem:
        item_list = ListMenuItem(self.central_widget, self.list_width, self.list_height, depth)
        item_list.setItemDelegate(MenuListItemsDelegate(self.item_height))
        # 列表内 item 事件
        item_list.itemClicked.connect(self.clicked_item_handle)
        item_list.setMouseTracking(True)
        item_list.itemEntered.connect(self.hover_item_handle)
        for item_text in data:
            item_abs_path = f"{abs_path}->{item_text}"
            # 如果仍是字典进行递归
            if isinstance(data[item_text], dict):
                list_item = MenuListItem(
                    f"↓↓ {item_text}", item_abs_path, depth,
                    self._load_data(data[item_text], item_abs_path, depth + 1),
                )
                pass
            # 注册事件
            else:
                list_item = MenuListItem(item_text, item_abs_path, depth)
                self.item_event_map[item_abs_path] = data[item_text]
                pass
            item_list.addItem(list_item)
            pass
        return item_list

    def load_data(self, data: dict[str, Callable[[], None] | Any]) -> None:
        self.root_list = self._load_data(data)
        self.root_list.setGeometry(0, 0, self.list_width, self.list_height)
        self.root_list.show()
        pass

    def clicked_item_handle(self, item: MenuListItem):
        if not item.item_list and item.item_abs_path in self.item_event_map:
            self.item_event_map[item.item_abs_path]()
            # # 判断方法调用的参数数量
            # sig = inspect.signature(call)
            # params = sig.parameters
            # if len(params) > 0:
            #     call(self)
            # else:
            #     call()
            pass
        pass

    def hover_item_handle(self, item: MenuListItem):
        if self.is_locked: return

        item_depth = item.item_depth
        if item.item_list:
            item_list = item.item_list

            if (
                    item_depth in self.pre_item_list_map and
                    self.pre_item_list_map[item_depth] is item_list and
                    item_list.isVisible()
            ): return

            # 隐藏低层级的显示列表
            for i_list in self.pre_item_list_map.values():
                if i_list.item_depth > item_depth:
                    i_list.hide()
                pass
            self.pre_item_list_map[item_depth] = item_list
            x = self.root_list.x() + (self.list_width + 3) * item_depth
            y = self.root_list.y() + self.item_height * item_depth
            if x + self.list_width > self.x() + self.width():
                if item_depth - 1 in self.pre_item_list_map:
                    x = min(self.pre_item_list_map[item_depth - 1].x(), self.root_list.x()) - self.list_width - 3
                else:
                    x = self.root_list.x() - self.list_width - 3
                pass
            excess_y = y + self.list_height - self.y() - self.height()
            if excess_y > 0: y -= excess_y
            item_list.move(x, y)
            item_list.show()
            pass
        else:
            for i_list in self.pre_item_list_map.values():
                if i_list.item_depth > item_depth:
                    i_list.hide()
                pass
            pass
        pass

    def show(self):
        super().show()
        self.is_locked = False

        x = config.mouse_x
        y = config.mouse_y
        excess_x = x + self.list_width - self.x() - self.width()
        excess_y = y + self.list_height - self.y() - self.height()
        if excess_x > 0: x -= excess_x
        if excess_y > 0: y -= excess_y
        self.root_list.move(x, y)
        self.root_list.show()
        pass

    def hide(self):
        self.is_locked = True

        super().hide()
        self.root_list.hide()
        for i_list in self.pre_item_list_map.values():
            i_list.hide()
        self.pre_item_list_map.clear()
        pass

    def closeEvent(self, a0):
        self.is_locked = True

        super().closeEvent(a0)
        self.root_list.hide()
        for i_list in self.pre_item_list_map.values():
            i_list.hide()
        self.pre_item_list_map.clear()
        pass

    pass
