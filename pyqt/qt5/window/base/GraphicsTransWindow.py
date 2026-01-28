from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene


class GraphicsTransWindow(QGraphicsView):

    def __init__(self, x: int, y: int, w: int, h: int):
        super(GraphicsTransWindow, self).__init__()
        self.setGeometry(x, y, w, h)

        self._init_window()

        # 显示窗口动画
        self.show_anim = QPropertyAnimation(self, b"windowOpacity")
        self.show_anim.setEasingCurve(QEasingCurve.OutSine)
        self.show_anim.setDuration(300)
        self.show_anim.setStartValue(0.0)
        self.show_anim.setEndValue(1.0)
        self.show_anim.finished.connect(super().show)

        # 隐藏窗口动画
        self.hide_anim = QPropertyAnimation(self, b"windowOpacity")
        self.hide_anim.setEasingCurve(QEasingCurve.InSine)
        self.hide_anim.setDuration(300)
        self.hide_anim.setStartValue(1.0)
        self.hide_anim.setEndValue(0.0)
        self.hide_anim.finished.connect(self.hide)

        # 创建场景
        self.scene = QGraphicsScene(0, 0, w, h)
        self.scene.setBackgroundBrush(QBrush(Qt.transparent))
        self.setScene(self.scene)
        pass

    def _init_window(self):
        # 设置窗口标识
        self.setWindowFlags(
            Qt.Window |
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        # 设置框架样式为无
        self.setFrameShape(QGraphicsView.NoFrame)

        # 设置视口（Viewport）透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState)

        # 设置渲染优化
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.setViewportUpdateMode(self.FullViewportUpdate)  # 减少闪烁
        pass

    def paintEvent(self, event):
        """重写paintEvent确保透明背景绘制"""
        # 先清空背景
        painter = QPainter(self.viewport())
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(event.rect(), Qt.transparent)
        painter.end()

        # 调用父类的绘制
        super().paintEvent(event)
        pass

    def toggle_visibility(self):
        if self.isVisible():
            self.close()
        else:
            self.show()
            pass
        pass

    def show(self):
        super().show()
        self.raise_()  # 将窗口提到前面
        self.activateWindow()  # 激活窗口
        pass

    def showEvent(self, event):
        self.show_anim.start()
        pass

    def closeEvent(self, a0):
        """重写关闭事件，隐藏窗口而不是关闭"""
        a0.ignore()
        self.hide_anim.start()
        pass

    pass
