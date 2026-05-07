class ChatWidgetMessage:
    def __init__(self, text: str, avatar: str = None, is_self: bool = False):
        self.text: str = text
        self.is_self: bool = is_self
        self.avatar: str = avatar
        pass

    pass
