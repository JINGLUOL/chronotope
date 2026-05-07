from PyQt5.QtCore import QAbstractListModel, QModelIndex

from .ChatMap import ChatMap


class ChatModel(QAbstractListModel):

    def __init__(self, messages=None, parent=None):
        super(ChatModel, self).__init__(parent)
        self._messages: list[dict] = messages or []
        pass

    def rowCount(self, parent=...):
        return len(self._messages)

    def data(self, index, role=...):
        if not index.isValid():
            return None

        message = self._messages[index.row()]
        if role == ChatMap.TextRole:
            return message["text"]
        elif role == ChatMap.IsSelfRole:
            return message["is_self"]
        elif role == ChatMap.AvatarRole:
            return message["avatar"]
        elif role == ChatMap.SenderRole:
            return message["sender"]
        elif role == ChatMap.TimestampRole:
            return message["timestamp"]
        return None

    def add_message(self, message):
        """向模型追加一条新消息。"""
        # 1. 获取新行位置
        row = self.rowCount()
        # 2. 开始插入操作，通知视图
        self.beginInsertRows(QModelIndex(), row, row)
        # 3. 修改底层数据
        self._messages.append(message)
        # 4. 结束插入，视图会刷新显示
        self.endInsertRows()
        pass

    def add_pre_messages(self, messages):
        """向模型插入历史消息。"""
        pre_len = len(messages)
        self.beginInsertRows(QModelIndex(), 0, pre_len)
        messages.extend(self._messages)
        self._messages = messages
        self.endInsertRows()
        pass

    pass
