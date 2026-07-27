class JSONObject:

    def __init__(self, data: dict):
        for k, v in data.items(): setattr(self, k, v)
        pass

    pass
