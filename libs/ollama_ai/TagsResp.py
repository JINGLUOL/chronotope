from libs.jing_luo.json import JSONObject


class Model(JSONObject):
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: dict

    def __init__(self, data: dict):
        super().__init__(data)
        pass

    pass


class TagsResp(JSONObject):
    models: list

    def __init__(self, data):
        super().__init__(data)

        self.models = [Model(model) for model in self.models]
        pass

    pass
