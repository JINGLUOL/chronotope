from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QLinearGradient


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

    painter.setBrush(QBrush(gradient))
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
