from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget


class LoadingCircle(QWidget):

    def __init__(
            self,
            bar_color: QColor = QColor(0, 150, 255),
            bg_color: QColor | None = None,
            parent=None
    ):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_angle)
        self.setFixedSize(80, 80)

        self.bar_color = bar_color
        ''' 进度条颜色 '''
        self.bg_color = bg_color
        ''' 背景颜色 '''
        pass

    def run(self):
        self.timer.start(50)  # 每50ms更新一次，控制旋转速度
        pass

    def completed(self):
        self.timer.stop()
        self.angle = 360
        self.update()
        pass

    def update_angle(self):
        self.angle = (self.angle + 10) % 360
        self.update()
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 绘制背景（可选）
        # painter.setBrush(self.bg_color)
        # painter.drawEllipse(self.rect())
        # 绘制圆弧
        pen = QPen(self.bar_color, 6, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        rect = QRectF(21, 21, self.width() - 43, self.height() - 43)
        # 绘制从 0 到 270 度的圆弧（留出缺口形成旋转效果）
        painter.drawArc(rect, self.angle * 16, 270 * 16)  # 16是角度单位转换
        pass

    pass
