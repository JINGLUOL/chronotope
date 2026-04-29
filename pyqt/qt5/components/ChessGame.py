from dataclasses import dataclass

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsPixmapItem, QVBoxLayout

from pyqt.qt5.window import TransparentWindow


@dataclass
class GameModels:
    GO_GAME: str = 'GO_GAME'
    pass


@dataclass
class ChessPiece:
    """围棋逻辑核心：棋盘状态、落子、提子、劫争、胜负判定"""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    pass


class GoGame:

    def __init__(self):
        self.chessboard: [[int]] = []
        self.current_player: int = ChessPiece.BLACK
        pass

    pass


class ChessGame(TransparentWindow):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        self.node_size: int = 3
        ''' 节点大小 '''
        self.s_node_size: int = 7
        ''' 星位（天元、小目）大小 '''
        self.grid_size: int = 13
        ''' 方格大小 '''
        self.chess_size: int = 19
        ''' 棋盘大小 '''

        self.game_model: str = GameModels.GO_GAME
        pass

    def paintEvent(self, a0):
        painter = QPainter(self)
        pass

    def draw_board(self, painter: QPainter):
        for i in range(self.chess_size):
            pass
        pass

    pass
