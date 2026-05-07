from dataclasses import dataclass


@dataclass
class ChessPiece:
    """围棋逻辑核心：棋盘状态、落子、提子、劫争、胜负判定"""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    pass
