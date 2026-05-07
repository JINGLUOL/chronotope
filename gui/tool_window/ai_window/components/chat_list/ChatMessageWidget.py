from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QListWidgetItem


class ChatMessageWidget(QWidget):

    def __init__(self, avatar: QPixmap, text: str, is_self: bool, list_item: QListWidgetItem, parent=None):
        super(ChatMessageWidget, self).__init__(parent)

        # 创建布局
        layout = QHBoxLayout(self)

        # 头像标签
        icon_label = QLabel()
        icon_label.setPixmap(avatar)
        icon_label.setAlignment(Qt.AlignTop)

        # 消息体标签
        self.msg_label = msg_label = QLabel(text)
        self.msg_label.setMaximumWidth(self.parent().width() - 99)
        msg_label.setWordWrap(True)  # 开启自动换行
        msg_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # 根据消息来源（自己发送或对方发送）决定布局方向和样式
        if is_self:
            msg_label.setObjectName("chat_message_s")
            layout.addStretch(1)
            layout.addWidget(msg_label)
            layout.addWidget(icon_label)
        else:
            layout.addWidget(icon_label)
            layout.addWidget(msg_label)
            layout.addStretch(1)
            msg_label.setObjectName("chat_message_o")

        self.list_item = list_item
        self._update_list_item_size()
        pass

    def _update_list_item_size(self):
        """ 设置组件尺寸提示，确保列表项高度正确 """
        self.list_item.setSizeHint(self.sizeHint())
        pass

    def update_msg(self, new_msg: str):
        self.msg_label.setText(new_msg)
        self._update_list_item_size()
        pass

    pass
