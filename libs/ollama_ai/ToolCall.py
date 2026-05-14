class Function:
    index: int = 0
    name: str = None
    arguments: dict = None

    def __init__(self, data):
        for key, value in data.items(): setattr(self, key, value)
        pass

    pass


class ToolCall:
    id: str = None
    function: Function | dict = None

    def __init__(self, data):
        for key, value in data.items(): setattr(self, key, value)

        if self.function: self.function = Function(self.function)
        pass

    pass
