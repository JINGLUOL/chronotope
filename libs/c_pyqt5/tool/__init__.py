__all__ = [
    'create_gradient_pixmap',
    'create_default_avatar_pixmap',
    'timer',
    'InputAreaDialog',
    'ImageDialog'
]

from .ImageDialog import ImageDialog
from .InputAreaDialog import InputAreaDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QFont, QFontMetrics

from .Timer import timer


def create_gradient_pixmap(
        w: int, h: int,
        gradient: QLinearGradient,
        flags: int = Qt.AlignCenter, text: str = None,
        text_size: int = 7, text_bold: bool = False,
        text_color: QColor = Qt.gray,
) -> QPixmap:
    """创建渐变背景的图片"""
    pixmap = QPixmap(w, h)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    painter.setBrush(gradient)
    painter.setPen(Qt.NoPen)
    painter.drawRect(0, 0, w, h)

    # 添加文字
    if text:
        painter.setPen(text_color)
        font = painter.font()
        font.setPointSize(text_size)
        font.setBold(text_bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), flags, text)
        pass

    painter.end()
    return pixmap


def create_default_avatar_pixmap(size=50):
    # 1. 创建 QPixmap
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.white)

    # 2. 开始绘制
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

    # 3. 设置字体
    painter.setPen(Qt.black)
    font = QFont("Arial", int(size * 0.35), QFont.Bold)  # 字体大小约为图片尺寸的60%
    painter.setFont(font)

    # 4. 计算文字矩形，使其居中
    text = "?"
    fm = QFontMetrics(font)
    text_rect = fm.boundingRect(text)
    x = (size - text_rect.width()) // 2
    y = (size - text_rect.height()) // 2 + fm.ascent()

    # 5. 绘制文字
    painter.drawText(x, y, text)

    # 6. 结束绘制
    painter.end()
    return pixmap
