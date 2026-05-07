class Model:
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: dict

    def __init__(self, data: dict):
        for key, value in data.items(): setattr(self, key, value)
        pass

    pass


class TagsResp:
    models: list

    def __init__(self, data):
        for key, value in data.items(): setattr(self, key, value)
        self.models = [Model(model) for model in self.models]
        pass

    pass
