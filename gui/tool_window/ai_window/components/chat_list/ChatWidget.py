from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QAbstractItemView

from app_work.tool_work.ai_window_work import ChatWidgetMessage
from libs.c_pyqt5.tool import create_default_avatar_pixmap
from .ChatMessageWidget import ChatMessageWidget


class ChatWidget(QWidget):
    update_message_slot = pyqtSignal(ChatWidgetMessage)

    def __init__(self, parent=None):
        super(ChatWidget, self).__init__(parent)

        # 创建 QListWidget 作为聊天消息列表容器
        self.chat_list = QListWidget(self)
        self.chat_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 设置按像素滚动

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.chat_list)
        self.DEFAULT_AVATAR = create_default_avatar_pixmap()

        self.pre_bubble: ChatMessageWidget | None = None

        self.update_message_slot.connect(self._update_message)
        pass

    def _update_message(self, msg: ChatWidgetMessage):
        self.pre_bubble.update_msg(msg.text)
        pass

    def add_message(self, msg: ChatWidgetMessage):
        """向聊天列表中添加一条消息"""
        # 创建 QListWidgetItem
        item = QListWidgetItem()
        # 将组件添加到 QListWidget
        self.chat_list.addItem(item)
        # 创建自定义气泡组件
        bubble = ChatMessageWidget(
            msg.avatar or self.DEFAULT_AVATAR,
            msg.text, msg.is_self, item, self.chat_list
        )
        self.chat_list.setItemWidget(item, bubble)
        self.pre_bubble = bubble
        pass

    def add_pre_messages(self, messages: list[ChatWidgetMessage]):
        """向聊天列表中添加历史消息"""
        for msg in messages:
            # 创建 QListWidgetItem
            item = QListWidgetItem()
            # 将组件添加到 QListWidget
            self.chat_list.insertItem(0, item)
            # 创建自定义气泡组件
            bubble = ChatMessageWidget(msg.avatar or self.DEFAULT_AVATAR, msg.text, msg.is_self, item)
            self.chat_list.setItemWidget(item, bubble)
        pass

    pass
