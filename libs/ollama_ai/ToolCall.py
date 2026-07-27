from libs.jing_luo.json import JSONObject


class Function(JSONObject):
    index: int = 0
    name: str = None
    arguments: dict = None

    def __init__(self, data):
        super().__init__(data)
        pass

    pass


class ToolCall(JSONObject):
    id: str = None
    function: Function | dict = None

    def __init__(self, data):
        super().__init__(data)

        if self.function: self.function = Function(self.function)
        pass

    pass
