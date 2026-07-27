from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter, QPen, QConicalGradient, QColor, QBrush
from PyQt5.QtWidgets import QWidget


class CircleBar(QWidget):
    def __init__(self, parent=None):
        super(CircleBar, self).__init__(parent)
        # 默认值设置
        self.value = 0
        self.min_val = 0
        self.max_val = 100
        self.bar_width = 10
        self.text_visible = True

        # 颜色设置
        self.progress_color = QColor(0, 120, 215)  # 进度颜色
        self.bg_color = QColor(230, 230, 230)      # 背景颜色
        self.text_color = QColor(50, 50, 50)       # 文字颜色
        pass

    def set_value(self, value):
        self.value = max(self.min_val, min(value, self.max_val))
        self.update()  # 触发重绘
        pass

    def paintEvent(self, event):
        # 获取可用区域
        width = min(self.width(), self.height()) - 4
        rect = QRectF(2, 2, width, width)
        start_angle = 90 * 16  # 起始角度（顶部为0°，但PyQt从90°开始更自然）

        # 计算进度角度（360°对应100%）
        span_angle = -self.value / (self.max_val - self.min_val) * 360 * 16

        # 开始绘制
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景圆
        pen = QPen()
        pen.setWidth(self.bar_width)
        pen.setColor(self.bg_color)
        painter.setPen(pen)
        painter.drawArc(rect, 0, 360 * 16)

        # 绘制进度弧（使用锥形渐变实现平滑过渡）
        gradient = QConicalGradient(self.rect().center(), 90)
        gradient.setColorAt(0, self.progress_color)
        gradient.setColorAt(1, self.progress_color.darker(120))

        pen.setColor(QColor(0, 0, 0, 0))  # 透明边框确保渐变连续
        painter.setPen(pen)
        painter.setBrush(QBrush(gradient))
        painter.drawPie(rect, start_angle, span_angle)
        pass
