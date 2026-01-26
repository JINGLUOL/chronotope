class Rect:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        pass

    @classmethod
    def from_pos_and_size(cls, pos: tuple[int, int], size: tuple[int, int]):
        return cls(pos[0], pos[1], size[0], size[1])

    def include(self, x, y):
        return 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h

    def point_directions(self, x, y) -> tuple[bool, bool, bool, bool]:
        """ 返回点在矩形上下和左右的布尔值 """
        return y < self.y, y > self.y + self.h, x < self.x, x > self.x + self.w

    def __add__(self, other):
        """ 加法运算 """
        if isinstance(other, (int, float)):
            return Rect(self.x - other, self.y - other, self.w + other*2, self.h + other*2)
        elif isinstance(other, Rect):
            return Rect(self.x - other.w, self.y - other.h, self.w + other.w, self.h + other.h)
        pass

    def __radd__(self, other):
        """ 反方位加法 """
        return self.__add__(other)

    def __sub__(self, other):
        """ 减法运算 """
        pass

    def __rsub__(self, other):
        return self.__sub__(other)

    # 用户友好的字符串表示
    def __str__(self):
        return f"Rect: {self.x}, {self.y}, {self.w}, {self.h}"

    # 开发者友好的字符串表示
    def __repr__(self):
        return f"Rect(x={self.x}, y={self.y}, w={self.w}, h={self.h})"

    pass
