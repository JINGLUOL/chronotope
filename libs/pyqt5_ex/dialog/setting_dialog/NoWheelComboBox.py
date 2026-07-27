from PyQt5.QtWidgets import QComboBox


class NoWheelComboBox(QComboBox):

    def wheelEvent(self, event):
        # 忽略滚轮事件，什么都不做
        event.ignore()
        pass

    pass
