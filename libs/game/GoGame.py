from collections import deque

from .ChessPiece import ChessPiece


class GoGame:

    def __init__(self, size: int = 19):
        self.size: int = size
        ''' 棋盘大小 '''
        self.chessboard: list[list[int]] = [[ChessPiece.EMPTY] * size for _ in range(size)]
        ''' 棋盘数据 '''
        self.current_player: int = ChessPiece.BLACK
        ''' 当前玩家 '''
        self.history: deque[tuple[int, int]] = deque(maxlen=3)
        ''' 历史步数 '''
        self.last_history: tuple[int, int] | None = None
        ''' 历史最后一步 '''
        self.black_captured: int = 0
        ''' 黑棋棋获 '''
        self.white_captured: int = 0
        ''' 白棋棋获 '''
        self.pass_count: int = 0
        ''' 累计回合跳过数 '''
        self.game_over: bool = False
        pass

    def reset_game(self):
        self.chessboard = [[ChessPiece.EMPTY] * self.size for _ in range(self.size)]
        self.current_player = ChessPiece.BLACK
        self.history.clear()
        self.last_history = None
        self.black_captured = 0
        self.white_captured = 0
        self.pass_count = 0
        self.game_over = False
        pass

    def pass_move(self) -> int | None:
        """ 跳过当前回合 """
        if self.game_over:
            return None
        self.pass_count += 1
        if self.pass_count == 2:
            self.game_over = True
            black_score, white_score = self.calculate_scores()
            if black_score > white_score:
                return ChessPiece.BLACK
            elif white_score > black_score:
                return ChessPiece.WHITE
            else:
                return ChessPiece.EMPTY  # 平局
        else:
            self.current_player = self.get_opponent()
        return None

    def calculate_scores(self) -> dict[int, int]:
        """数子法（中国规则）：子空皆地，黑贴7.5目（3.75子）"""
        # 计算盘面棋子数 + 领地（空点归属）
        territory = self.calculate_territory()
        black_stones = sum(row.count(ChessPiece.BLACK) for row in self.chessboard)
        white_stones = sum(row.count(ChessPiece.WHITE) for row in self.chessboard)
        black_total = black_stones + territory[ChessPiece.BLACK]
        white_total = white_stones + territory[ChessPiece.WHITE]
        # 黑贴7.5目（3.75子）
        black_total -= 3.75
        return {ChessPiece.BLACK: black_total, ChessPiece.WHITE: white_total}

    def calculate_territory(self):
        """计算空点的归属（简单 flood fill）"""
        visited = [[False] * self.size for _ in range(self.size)]
        territory = {ChessPiece.BLACK: 0, ChessPiece.WHITE: 0}
        for i in range(self.size):
            for j in range(self.size):
                if self.chessboard[i][j] == ChessPiece.EMPTY and not visited[i][j]:
                    # 开始 BFS 找出连通空域
                    queue = deque()
                    queue.append((i, j))
                    visited[i][j] = True
                    empty_cells = [(i, j)]
                    boundary_colors = set()
                    while queue:
                        r, c = queue.popleft()
                        for nr, nc in self.get_neighbors(r, c):
                            if self.chessboard[nr][nc] == ChessPiece.EMPTY and not visited[nr][nc]:
                                visited[nr][nc] = True
                                queue.append((nr, nc))
                                empty_cells.append((nr, nc))
                            elif self.chessboard[nr][nc] != ChessPiece.EMPTY:
                                boundary_colors.add(self.chessboard[nr][nc])
                    # 如果边界只有一种颜色，则这片空域归该颜色所有
                    if len(boundary_colors) == 1:
                        territory[boundary_colors.pop()] += len(empty_cells)
        return territory

    def is_suicide(self, x, y) -> bool:
        """判断在 (row, col) 落子是否自杀（落子后自己的块气为0且没有提掉对方）"""
        if (x, y) in self.history: return True  # 劫争判断

        # 模拟落子
        self.chessboard[x][y] = self.current_player
        # 获取自己所在的组
        group = self.get_group(x, y)
        libs = self.get_liberties(group)
        # 判断是否有提掉对方棋子
        captured_any = False
        for nr, nc in self.get_neighbors(x, y):
            if self.chessboard[nr][nc] == self.get_opponent():
                opp_group = self.get_group(nr, nc)
                if len(self.get_liberties(opp_group)) == 0: captured_any = True
                pass
            pass
        self.chessboard[x][y] = ChessPiece.EMPTY  # 撤销模拟
        return len(libs) == 0 and not captured_any

    def get_group(self, row, col):
        """返回包含 (row, col) 的连通块（相同颜色）的所有坐标"""
        color = self.chessboard[row][col]
        if color is ChessPiece.EMPTY:
            return []
        visited = set()
        queue = deque()
        queue.append((row, col))
        visited.add((row, col))
        while queue:
            r, c = queue.popleft()
            for nr, nc in self.get_neighbors(r, c):
                if (nr, nc) not in visited and self.chessboard[nr][nc] == color:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return list(visited)

    def remove_group(self, group):
        for r, c in group:
            self.chessboard[r][c] = ChessPiece.EMPTY
        if self.current_player == ChessPiece.BLACK:
            self.black_captured += len(group)
        else:
            self.white_captured += len(group)
        pass

    def get_liberties(self, group):
        """计算一个连通块的气（相邻空点的集合）"""
        liberties = set()
        for r, c in group:
            for nr, nc in self.get_neighbors(r, c):
                if self.chessboard[nr][nc] == ChessPiece.EMPTY:
                    liberties.add((nr, nc))
        return liberties

    def is_on_board(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def get_neighbors(self, row, col):
        """返回上下左右四个方向的坐标列表（仅限棋盘内）"""
        res = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if self.is_on_board(r, c):
                res.append((r, c))
        return res

    def get_opponent(self, current_player=None):
        """ 获取对手 """
        if current_player is None: current_player = self.current_player
        return ChessPiece.WHITE if current_player is ChessPiece.BLACK else ChessPiece.BLACK

    def get_piece(self, x: int, y: int) -> int:
        """ 获取棋子 """
        return self.chessboard[x][y]

    def set_piece(self, x: int, y: int) -> bool:
        """ 落子 """
        pos = (x, y)
        if self.game_over:
            return False
        elif self.chessboard[x][y] != ChessPiece.EMPTY:
            return False
        elif self.is_suicide(x, y):
            return False

        ''' 执行落子 '''
        self.history.append(pos)  # 记录步数
        self.last_history = pos
        self.chessboard[x][y] = self.current_player  # 落子
        self.pass_count = 0
        ''' 提掉相邻无气的对方棋子 '''
        opponents = []
        for nr, nc in self.get_neighbors(x, y):
            if self.chessboard[nr][nc] == self.get_opponent():
                group = self.get_group(nr, nc)
                if len(self.get_liberties(group)) == 0: opponents.append(group)
                pass
            pass
        for group in opponents: self.remove_group(group)

        self.current_player = self.get_opponent()  # 切换玩家
        return True

    pass
