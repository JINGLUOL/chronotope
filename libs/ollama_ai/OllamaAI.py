import json
from typing import Callable

import requests


class OllamaAI:

    def __init__(self, model: str = None):
        self.ip = 'localhost'
        ''' 访问地址 '''
        self.port = 11434
        ''' 访问端口 '''
        self.model: str | None = model
        ''' 当前询问的模型id '''
        self.stream: bool = True
        ''' 是否使用流式输出 '''
        pass

    def _get_url(self, api):
        return f'http://{self.ip}:{self.port}{api}'

    def _get(self, api):
        try:
            resp = requests.get(self._get_url(api))
            return resp.json() if resp.status_code == 200 else None
        except requests.exceptions.RequestException:
            print("Network anomaly")
        return None

    def _post(self, api: str, data: str, callback: Callable[[str], None]) -> bool:
        try:
            if self.stream:
                with requests.post(
                        url=self._get_url(api),
                        data=data,
                        stream=self.stream,
                ) as resp:
                    if resp.status_code != 200: return False
                    for line in resp.iter_lines(decode_unicode=True):
                        if line: callback(json.loads(line))
                    pass
                return True
            else:
                resp = requests.post(
                    url=self._get_url(api),
                    data=data,
                    stream=self.stream,
                )
                if resp.status_code != 200: return False
                callback(json.loads(resp.text))
                return True
        except requests.exceptions.RequestException:
            print("Network anomaly")
        return False

    def tags(self):
        """ 获取所有的模型列表 """
        return self._get("/api/tags")

    def ps(self):
        """ 获取激活的模型列表 """
        return self._get("/api/ps")

    def generate(self, data: str, callback: Callable[[str], None]):
        """ 生成 """
        data = json.dumps({
            "model": self.model,
            "prompt": data,
            "stream": self.stream,
        })
        return self._post("/api/generate", data, callback)

    def chat(self, data: list[dict], callback: Callable[[str], None]):
        """ 聊天 """
        data = json.dumps({
            "model": self.model,
            "messages": data,
            "stream": self.stream,
        })
        return self._post("/api/chat", data, callback)

    pass
