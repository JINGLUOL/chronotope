from PyQt5.QtGui import QColor, QLinearGradient, QPen, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem, QGraphicsRectItem


class GraphicsTextRectItem:

    def __init__(
            self, scene: QGraphicsScene, width: int, height: int,
            text_color: QColor = QColor(255, 255, 255),
            bg_color: QColor | QLinearGradient = QColor(0, 0, 0)
    ) -> None:
        self.text_item = QGraphicsSimpleTextItem()
        self.item_bg = QGraphicsRectItem(0, 0, width, height)

        self.text_item.setBrush(text_color)
        self.item_bg.setBrush(bg_color)

        scene.addItem(self.text_item)
        scene.addItem(self.item_bg)

        self.set_z_value(1)
        pass

    def x(self):
        return self.item_bg.x()

    def y(self):
        return self.item_bg.y()

    def get_text(self):
        return self.text_item.text()

    def set_font(self, font: QFont):
        self.text_item.setFont(font)
        pass

    def set_text(self, text: str):
        self.text_item.setText(text)
        self.set_pos(self.item_bg.x(), self.item_bg.y())
        pass

    def set_pen(self, pen: QPen):
        self.item_bg.setPen(pen)
        pass

    def set_pos(self, x: float, y: float):
        rect = self.item_bg.rect()
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos(
            x + rect.width() / 2 - text_rect.width() / 2,
            y + rect.height() / 2 - text_rect.height() / 2
        )
        self.item_bg.setPos(x, y)
        pass

    def set_z_value(self, z: float):
        self.text_item.setZValue(z)
        self.item_bg.setZValue(z - 1)
        pass

    def move(self, x: float, y: float):
        self.text_item.moveBy(x, y)
        self.item_bg.moveBy(x, y)
        pass

    def hide(self):
        self.text_item.hide()
        self.item_bg.hide()
        pass

    def show(self):
        self.text_item.show()
        self.item_bg.show()
        pass

    def remove(self):
        if self.text_item.scene():
            self.text_item.scene().removeItem(self.text_item)
        if self.item_bg.scene():
            self.item_bg.scene().removeItem(self.item_bg)
        pass

    pass
