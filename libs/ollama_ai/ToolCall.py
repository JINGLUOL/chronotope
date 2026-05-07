class ToolCall:
    name = None
    description = None
    arguments = None

    def __init__(self, data):
        for key, value in data.items(): setattr(self, key, value)
        pass

    pass
