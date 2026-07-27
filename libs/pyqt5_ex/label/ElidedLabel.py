from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QFontMetrics


class ElidedLabel(QLabel):
    """ 弹性内容标签 """

    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._full_text = text
        self._elide_mode = Qt.ElideRight  # 省略方式：左、中、右
        self.setText(text)  # 初始显示完整文本（但会触发paintEvent）
        pass

    def set_elide_mode(self, mode):
        """设置省略模式：Qt.ElideLeft, Qt.ElideRight, Qt.ElideMiddle"""
        self._elide_mode = mode
        self.update()
        pass

    def setText(self, text):
        self._full_text = text
        self.update()
        pass

    def text(self):
        return self._full_text

    def paintEvent(self, event):
        painter = QPainter(self)
        opt = self.initPainter(painter)
        # 获取可用于绘制的矩形区域（去掉margin/padding）
        rect = self.contentsRect()
        # 获取当前字体的度量工具
        fm = QFontMetrics(self.font())
        # 计算省略后的文本
        elided = fm.elidedText(self._full_text, self._elide_mode, rect.width())
        # 绘制对齐方式
        painter.drawText(rect, self.alignment(), elided)
        pass

    def minimumSizeHint(self):
        # 返回省略后至少需要的宽度（取第一个字符宽度）
        fm = QFontMetrics(self.font())
        width = fm.horizontalAdvance('…') + 5
        return QSize(width, fm.height())

    pass
