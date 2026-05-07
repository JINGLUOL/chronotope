from PyQt5.QtWidgets import QListView

from .ChatDelegate import ChatDelegate
from .ChatModel import ChatModel


class ChatView(QListView):

    def __init__(self, parent=None):
        super(ChatView, self).__init__(parent)

        # 设置数据模型
        self.model = ChatModel()
        ''' 数据模型 '''
        self.setModel(self.model)

        # 设置列表项代理
        self.delegate = ChatDelegate()
        ''' 列表项代理 '''
        self.setItemDelegate(self.delegate)
        pass

    pass
