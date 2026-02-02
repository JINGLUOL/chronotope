from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QPixmap, QLinearGradient, QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsPixmapItem


class PianoKeySignals(QObject):
    """ 钢琴键的信号槽集合 """

    press_signal = pyqtSignal(str)
    """ 鼠标按下时的信号槽 """

    release_signal = pyqtSignal(str)
    """ 鼠标释放时的信号槽 """

    pass


class PianoKey(QGraphicsPixmapItem):
    """钢琴键基类"""

    def __init__(
            self,
            key_name: str, key_midi: int, key_style: QPixmap,
            key_border_gradient: QLinearGradient, key_border_width: int
    ):
        super(PianoKey, self).__init__(key_style)
        # 琴键键值
        self.key_name = key_name
        self.key_id = key_midi

        # 琴键事件
        self.signals: PianoKeySignals = PianoKeySignals()

        # 琴键外观样式参数
        self.key_style = key_style
        self.key_radius = 9

        # 琴键边框参数
        self.key_border_gradient = key_border_gradient
        self.key_border_width = key_border_width

        # 设置琴键默认外观
        self.setPixmap(key_style)
        pass

    def mousePressEvent(self, event):
        self.signals.press_signal.emit(self.key_name)
        pass

    def mouseReleaseEvent(self, event):
        self.signals.release_signal.emit(self.key_name)
        pass

    def paint(self, painter, option, widget):
        """重写绘制方法实现圆角效果"""
        # 保存painter状态
        painter.save()

        # 设置抗锯齿
        painter.setRenderHint(QPainter.Antialiasing)

        # 创建圆角矩形路径
        rect = self.boundingRect()

        path = QPainterPath()
        path.addRoundedRect(rect, self.key_radius, self.key_radius)

        # 设置裁剪路径
        painter.setClipPath(path)

        # 调用父类的paint方法绘制图片
        super().paint(painter, option, widget)

        # 绘制渐变边框
        pen = QPen(QBrush(self.key_border_gradient), self.key_border_width)
        painter.setPen(pen)
        painter.drawPath(path)

        # 恢复painter状态
        painter.restore()
        pass

    pass


keyboard_map = {
    Qt.Key_G: 'C4',
    Qt.Key_Y: 'C#4',

    Qt.Key_H: 'D4',
    Qt.Key_U: 'D#4',

    Qt.Key_J: 'E4',

    Qt.Key_K: 'F4',
    Qt.Key_O: 'F#4',

    Qt.Key_L: 'G4',
    Qt.Key_P: 'G#4',

    Qt.Key_Semicolon: 'A4',
    Qt.Key_BracketLeft: 'A#4',

    Qt.Key_Apostrophe: 'B4'
}
