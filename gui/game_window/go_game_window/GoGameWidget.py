from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QRadialGradient, QColor
from PyQt5.QtWidgets import QLabel, QWidget

from libs.game import GoGame, ChessPiece


class GoGameWidget(QWidget):

    def __init__(self, window, parent=None):
        super(GoGameWidget, self).__init__(parent)

        self.window = window
        self.drag_pos = None

        self.game = GoGame()

        self.grid_size: int = 39
        ''' 方格大小 '''
        self.line_size: int = self.grid_size * (self.game.size - 1)
        ''' 棋盘线条长度 '''
        self.piece_r: int = int(self.grid_size / 2 * 0.7)
        ''' 节点大小 '''
        self.star_r: int = int(self.grid_size / 2 * 0.3)
        ''' 星位（天元、小目）大小 '''

        self.margin: int = 77
        ''' 边缘大小 '''

        self.board_size = self.line_size + self.margin * 2
        self.setMinimumSize(self.board_size, self.board_size)
        self.setMaximumSize(self.board_size, self.board_size)

        self.panel = QLabel('黑棋执棋', self)
        self.panel.setAlignment(Qt.AlignCenter)
        self.set_panel()
        pass

    def set_panel(self):
        margin = int(self.margin * 0.3)
        x = self.margin + margin
        y = self.board_size - self.margin
        width = self.line_size - margin * 2
        self.panel.setGeometry(x, y, width, self.margin)
        pass

    def paintEvent(self, a0):
        painter = QPainter(self)
        self.draw_board(painter)
        self.draw_pieces(painter)
        # 当前回合
        current_player = '黑棋回合' if self.game.current_player is ChessPiece.BLACK else '白棋回合'
        scores = self.game.calculate_scores()
        b_scores = f"黑棋方得分: {scores[ChessPiece.BLACK]}"
        w_scores = f"白棋方得分: {scores[ChessPiece.WHITE]}"
        self.panel.setText('   '.join([
            current_player,
            b_scores,
            w_scores
        ]))
        pass

    def draw_board(self, painter: QPainter):
        """ 棋盘绘制 """
        painter.setPen(QPen(Qt.black, 1))
        margin = self.margin
        for i in range(self.game.size):
            start = QPoint(margin + i * self.grid_size, margin)
            end = QPoint(margin + i * self.grid_size, margin + self.line_size)
            painter.drawLine(start, end)
            start = QPoint(margin, margin + i * self.grid_size)
            end = QPoint(margin + self.line_size, margin + i * self.grid_size)
            painter.drawLine(start, end)
            pass
        # 画星位（天元、小目）
        star_points = [(3, 3), (15, 3), (3, 15), (15, 15), (9, 9)]  # 0-index
        if self.game.size == 19:
            star_points.extend([(3, 9), (9, 3), (15, 9), (9, 15)])
        for r, c in star_points:
            x = margin + c * self.grid_size
            y = margin + r * self.grid_size
            painter.setBrush(QBrush(Qt.black))
            painter.drawEllipse(QPoint(x, y), self.star_r, self.star_r)
            pass
        pass

    def draw_pieces(self, painter: QPainter):
        """ 棋子绘制 """
        for r in range(self.game.size):
            for c in range(self.game.size):
                piece = self.game.get_piece(r, c)
                if piece is ChessPiece.EMPTY: continue

                x = self.margin + r * self.grid_size
                y = self.margin + c * self.grid_size
                gradient = QRadialGradient(x - self.piece_r / 2, y - self.piece_r / 2, self.piece_r)
                if piece is ChessPiece.BLACK:
                    gradient.setColorAt(0, QColor(80, 80, 80))
                    gradient.setColorAt(1, QColor(20, 20, 20))
                else:
                    gradient.setColorAt(0, QColor(255, 255, 255))
                    gradient.setColorAt(1, QColor(200, 200, 200))
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPoint(x, y), self.piece_r, self.piece_r)
                pass
            pass
        pass

    def mousePressEvent(self, a0):
        if a0.button() != Qt.LeftButton: return

        x, y = a0.x() - self.margin, a0.y() - self.margin
        if 0 <= x <= self.line_size and 0 <= y <= self.line_size:
            o_x, o_y = x % self.grid_size, y % self.grid_size
            if self.piece_r * 2 < o_x + self.piece_r < self.grid_size or self.piece_r * 2 < o_y + self.piece_r < self.grid_size:
                return
            x, y = int(x / self.grid_size), int(y / self.grid_size)
            if o_x > self.piece_r: x += 1
            if o_y > self.piece_r: y += 1
            if self.game.set_piece(x, y):
                self.repaint()
                pass
            pass
        else:
            self.drag_pos = a0.globalPos() - self.window.frameGeometry().topLeft()
            pass
        pass

    def mouseMoveEvent(self, a0):
        if self.drag_pos: self.window.move(a0.globalPos() - self.drag_pos)
        pass

    def mouseReleaseEvent(self, a0):
        self.drag_pos = None
        pass

    pass
