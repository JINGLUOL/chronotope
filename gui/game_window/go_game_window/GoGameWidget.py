import re
from dataclasses import dataclass

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QRadialGradient, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QPushButton, QHBoxLayout, QMessageBox

from gui.tool_window import ai_window
from libs.game import GoGame, ChessPiece
from libs.game.ChessPiece import get_piece_text

GameModelsVal = ("单人", "多人", "AI")

# f"围棋游戏\n{self.user_piece}代表{user}，{opponent_piece}代表{opponent}\n，{}"
game_message = f"""陪我下一把围棋
{ChessPiece.EMPTY}代表空置；
{ChessPiece.BLACK}代表{get_piece_text(ChessPiece.BLACK)}；
{ChessPiece.WHITE}代表{get_piece_text(ChessPiece.WHITE)}；
"""


@dataclass
class GameModels:
    SinglePlay = GameModelsVal[0]
    MultiPlay = GameModelsVal[1]
    AIPlay = GameModelsVal[2]
    pass


class GoGameWidget(QWidget):

    def __init__(self, window, parent=None):
        super(GoGameWidget, self).__init__(parent)

        self.window = window
        self.drag_pos = None

        self.game = GoGame()
        ''' 游戏对象 '''
        self.user_piece = ChessPiece.BLACK
        ''' 用户棋子 '''
        self.is_started = False
        ''' 是否开局 '''
        self.first_send: bool = True
        ''' 第一次给AI发送 '''

        self.start_game_btn = QPushButton('开局')
        self.start_game_btn.clicked.connect(self._start_game)
        self.game_model = QComboBox()
        self.game_model.addItems(GameModelsVal)

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
        self.panel.setObjectName("transparent")
        self.panel.setAlignment(Qt.AlignCenter)

        self._init_controller()
        self._move_panel()
        pass

    def _init_controller(self):
        x = self.margin
        y = self.board_size - self.margin

        widget = QWidget(self)
        widget.setObjectName("transparent")
        widget.setGeometry(x, y, self.line_size, self.margin)
        layout = QHBoxLayout(widget)
        layout.addWidget(self.start_game_btn)
        layout.addWidget(QLabel('对弈状态：'))
        layout.addWidget(self.game_model)
        layout.addStretch(1)
        pass

    def _move_panel(self):
        y = int(self.margin * 0.05)
        self.panel.setGeometry(self.margin, y, self.line_size, self.margin)
        pass

    def _start_game(self):
        self._reset_game()
        self.user_piece = ChessPiece.BLACK if QMessageBox.question(
            self,  # 父窗口
            "选择执棋方",  # 对话框标题
            "是否选择先手？",  # 询问内容
            QMessageBox.Yes | QMessageBox.No,  # 显示"是"和"否"按钮
            QMessageBox.Yes  # 默认选中"否"
        ) == QMessageBox.Yes else ChessPiece.WHITE
        pass

    def _reset_game(self):
        self.game.reset_game()
        self.update()
        self.is_started = True

        if not self.first_send:
            ai = ai_window()
            if ai:
                ai.send_message(f"重置游戏，结算一下我们的游戏分数。")
                pass
            pass
        self.first_send = True
        pass

    def _ai_set_piece(self, msg: str):
        if not msg: return

        points = re.findall(r'\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)', msg)
        if not len(points): return
        row, col = points[-1]
        if self.game.set_piece(int(row), int(col)):
            self.update()
        else:
            self._run_ai()
        pass

    def _run_ai(self):
        if self.first_send:
            opponent_piece = self.game.get_opponent(self.user_piece)
            opponent = get_piece_text(opponent_piece)
            user = get_piece_text(self.user_piece)
            piece_message = f"你执{opponent}，我执{user}。\n棋盘：\n"
            board_message = '\n'.join(' '.join(map(str, row)) for row in self.game.chessboard)
            send_msg = f"{board_message}\n该你了。\n请说出你想要落子的点，格式：(行,列)"
            ai = ai_window()
            if ai:
                ai.send_message(game_message + piece_message + send_msg, self._ai_set_piece)
                self.first_send = False
                pass
            pass
        else:
            ai = ai_window()
            if ai: ai.send_message(str(self.game.last_history), self._ai_set_piece)
            pass
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

                row = self.margin + r * self.grid_size
                col = self.margin + c * self.grid_size
                gradient = QRadialGradient(col - self.piece_r / 2, row - self.piece_r / 2, self.piece_r)
                if piece is ChessPiece.BLACK:
                    gradient.setColorAt(0, QColor(80, 80, 80))
                    gradient.setColorAt(1, QColor(20, 20, 20))
                else:
                    gradient.setColorAt(0, QColor(255, 255, 255))
                    gradient.setColorAt(1, QColor(200, 200, 200))
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPoint(col, row), self.piece_r, self.piece_r)
                pass
            pass
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

    def mousePressEvent(self, a0):
        if a0.button() != Qt.LeftButton: return

        x, y = a0.x() - self.margin, a0.y() - self.margin
        if 0 <= x <= self.line_size and 0 <= y <= self.line_size:
            # 判断现在是否该落子
            current_game_model = GameModelsVal[self.game_model.currentIndex()]
            if (
                    not self.is_started or self.game.game_over or
                    (
                            current_game_model is not GameModels.SinglePlay and
                            self.user_piece != self.game.current_player
                    )
            ): return

            # 判断是否在落子位置
            o_x, o_y = x % self.grid_size, y % self.grid_size
            if (
                    self.piece_r * 2 < o_x + self.piece_r < self.grid_size or
                    self.piece_r * 2 < o_y + self.piece_r < self.grid_size
            ): return

            # 计算落子坐标
            x, y = int(x / self.grid_size), int(y / self.grid_size)
            if o_x > self.piece_r: x += 1
            if o_y > self.piece_r: y += 1

            # 落子
            if self.game.set_piece(y, x):
                # 重绘棋盘
                self.update()
                # 当对弈为AI时
                if current_game_model is GameModels.AIPlay: self._run_ai()
                pass
            pass
        else:
            # 设置拖拽相对坐标
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
