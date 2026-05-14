from dataclasses import dataclass


@dataclass
class Piece:
    """围棋逻辑核心：棋盘状态、落子、提子、劫争、胜负判定"""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    pass


@dataclass
class FunMap:
    GetBoard: str = "getBoard"
    SetPiece: str = "setPiece"
    pass


def get_piece_text(piece: int) -> str:
    if piece == Piece.BLACK:
        return '黑子'
    elif piece == Piece.WHITE:
        return '白子'
    else:
        return '气'


tools = [
    {
        "type": "function",
        "function": {
            "name": FunMap.GetBoard,
            "description": f"获取围棋棋盘上所有棋子。{
            get_piece_text(Piece.EMPTY)
            }：{Piece.EMPTY}，{
            get_piece_text(Piece.BLACK)
            }：{Piece.BLACK}，{
            get_piece_text(Piece.WHITE)
            }：{Piece.WHITE}",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": FunMap.SetPiece,
            "description": "落子",
            "parameters": {
                "type": "object",
                "properties": {
                    "row": {
                        "type": "integer",
                        "description": "棋盘的行数，行数从0开始"
                    },
                    "col": {
                        "type": "integer",
                        "description": "棋盘的列数，列数从0开始"
                    }
                },
                "required": ["row", "col"]
            }
        }
    }
]
