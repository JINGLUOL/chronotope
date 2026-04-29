from abc import abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem, QMenu, QAction, QWidget

from .SpriteStatus import SpriteStatus


class SpriteAbs(QGraphicsPixmapItem):

    def __init__(self, parent: QWidget):
        QGraphicsPixmapItem.__init__(self)
        self.parent = parent

        self.sprite_x = 0
        """ X 轴值 """
        self.sprite_y = 0
        """ Y 轴值 """
        self.click_offset_x = 0.0
        self.click_offset_y = 0.0

        self.sprite_state = SpriteStatus.IDLE
        """ 精灵状态 """
        self.pre_click_sprite_state = None
        """ 点击精灵前的状态 """

        self.transition_item: QGraphicsPixmapItem = QGraphicsPixmapItem()
        """ 过渡动画器 """
        self.effect_item: QGraphicsPixmapItem = QGraphicsPixmapItem()
        """ 效果动画器 """

        self.menu = QMenu()
        """ 精灵右键菜单 """
        self._init_context_menu()

        self.keys_pressed: set[int] = set()
        """ 键盘按下事件 """

        # 精灵行为钩子映射表
        self.sprite_behavior_map = {
            SpriteStatus.IDLE: self._sprite_idle_handle,
            SpriteStatus.FOLLOW: self._sprite_follow_handle,
            SpriteStatus.CALL: self._sprite_call_handle,
            SpriteStatus.CLICKED: self._sprite_click_handle,
        }
        pass

    def _init_context_menu(self):
        """ 设置菜单项 """

        def def0():
            self.sprite_state = SpriteStatus.IDLE
            pass

        def def1():
            self.sprite_state = SpriteStatus.FOLLOW
            pass

        def def2():
            self.sprite_state = SpriteStatus.CALL
            pass

        def def3():
            if self.scene():
                self.scene().removeItem(self)
            pass

        sprite_idle = QAction("等待", self.menu)
        sprite_idle.triggered.connect(def0)

        sprite_follow = QAction("跟随", self.menu)
        sprite_follow.triggered.connect(def1)

        sprite_call = QAction("操控", self.menu)
        sprite_call.triggered.connect(def2)

        sprite_del = QAction("删除", self.menu)
        sprite_del.triggered.connect(def3)

        self.menu.addAction(sprite_idle)
        self.menu.addSeparator()
        self.menu.addAction(sprite_follow)
        self.menu.addSeparator()
        self.menu.addAction(sprite_call)
        self.menu.addSeparator()
        self.menu.addAction(sprite_del)
        pass

    def contextMenuEvent(self, event):
        """ 右键菜单事件 """
        # 显示菜单
        self.menu.exec_(event.screenPos())
        event.accept()
        pass

    def sprite_behavior_handle(self):
        self.sprite_behavior_map[self.sprite_state]()
        pass

    @abstractmethod
    def _sprite_idle_handle(self):
        pass

    @abstractmethod
    def _sprite_follow_handle(self):
        """ 精灵跟随钩子 """
        pass

    @abstractmethod
    def _sprite_call_handle(self):
        """ 命令精灵钩子 """
        pass

    @abstractmethod
    def _sprite_click_handle(self):
        pass

    @abstractmethod
    def update_anim(self, current_time: float):
        """ 帧动画绘制方法 """
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pre_click_sprite_state = self.sprite_state
            self.sprite_state = SpriteStatus.CLICKED
        pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.sprite_state = self.pre_click_sprite_state
            self.pre_click_sprite_state = None
        pass

    pass
