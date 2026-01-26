class Rect:

    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.w = size[0]
        self.h = size[1]
        pass

    def include(self, x, y):
        return 0 <= x <= self.w and 0 <= y <= self.h

    def include_point(self, start_point: tuple[int, int], point: tuple[int, int]):
        return (
                start_point[0] <= point[0] <= start_point[0] + self.w and
                start_point[1] <= point[1] <= start_point[1] + self.h
        )

    pass
