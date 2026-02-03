from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QStyledItemDelegate, QAbstractItemView, QGraphicsOpacityEffect


class MenuListItemsDelegate(QStyledItemDelegate):

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


class ListMenuItem(QListWidget):

    def __init__(self, parent, width: int, height: int, item_depth: int):
        super().__init__(parent)
        self.setVisible(False)
        # 禁用选择
        self.setSelectionMode(QAbstractItemView.NoSelection)
        # 关闭滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 创建透明度效果实例
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self.opacity_effect)

        # 显示窗口动画
        self.show_anim = QPropertyAnimation(self, b"geometry")
        self.show_anim.setEasingCurve(QEasingCurve.OutSine)
        self.show_anim.setDuration(300)
        self.show_opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.show_opacity_anim.setEasingCurve(QEasingCurve.OutSine)
        self.show_opacity_anim.setDuration(300)
        self.show_opacity_anim.setStartValue(0.0)
        self.show_opacity_anim.setEndValue(1.0)

        # 隐藏窗口动画
        self.hide_anim = QPropertyAnimation(self, b"geometry")
        self.hide_anim.setEasingCurve(QEasingCurve.InSine)
        self.hide_anim.setDuration(150)
        self.hide_opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.hide_opacity_anim.setEasingCurve(QEasingCurve.InSine)
        self.hide_opacity_anim.setDuration(150)
        self.hide_opacity_anim.setStartValue(1.0)
        self.hide_opacity_anim.setEndValue(0.0)
        self.hide_opacity_anim.finished.connect(super().hide)

        self.setGeometry(0, 0, width, height)
        self.item_depth = item_depth
        pass

    def showEvent(self, a0):
        super().showEvent(a0)
        self.show_anim.setStartValue(QRect(self.x(), self.y() - 33, self.width(), self.height()))
        self.show_anim.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.show_anim.start()
        self.show_opacity_anim.start()
        pass

    def hide(self):
        self.hide_anim.setStartValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.hide_anim.setEndValue(QRect(self.x(), self.y() - 33, self.width(), self.height()))
        self.hide_anim.start()
        self.hide_opacity_anim.start()
        pass

    pass


class MenuListItem(QListWidgetItem):

    def __init__(self, text: str, item_abs_path, item_depth: int, item_list: ListMenuItem = None):
        super().__init__(text)

        self.item_depth: int = item_depth
        """ 组件相对于根目录的深度 """
        self.item_abs_path = item_abs_path
        """ 组件相对于根目录的路径 """
        self.item_list = item_list
        """ 组件的下级列表 """
        pass

    pass
