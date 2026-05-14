import json
from typing import Callable, Any

import requests


class OllamaAI:

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        pass

    def _get_url(self, api):
        return f'{self.base_url}/{api}'

    def _get(self, api):
        try:
            resp = requests.get(self._get_url(api))
            return resp.json() if resp and resp.status_code == 200 else None
        except requests.exceptions.RequestException:
            print("Network anomaly")
        return None

    def _post(self, api: str, data: str, callback: Callable[[Any], None], stream: bool) -> bool:
        try:
            if stream:
                with requests.post(
                        url=self._get_url(api),
                        data=data,
                        stream=stream,
                ) as resp:
                    if not resp or resp.status_code != 200: return False
                    for line in resp.iter_lines(decode_unicode=True):
                        if line: callback(json.loads(line))
                    pass
                return True
            else:
                resp = requests.post(
                    url=self._get_url(api),
                    data=data,
                    stream=stream,
                )
                if not resp or resp.status_code != 200:
                    print(resp.text)
                    return False
                return json.loads(resp.text)
        except requests.exceptions.RequestException:
            print("Network anomaly")
        return False

    def delete(self, model: str):
        api = "/api/delete"
        data = json.dumps({'model': model, })
        try:
            resp = requests.delete(self._get_url(api), data=data)
            if resp and resp.status_code == 200:
                return True
            print(resp.text)
            return False
        except requests.exceptions.RequestException:
            print("Network anomaly")
        return None

    def tags(self):
        """ 获取所有的模型列表 """
        return self._get("/api/tags")

    def ps(self):
        """ 获取激活的模型列表 """
        return self._get("/api/ps")

    def generate(
            self,
            model: str, data: list[dict],
            callback: Callable[[Any], None], stream: bool = True
    ) -> Any:
        """ 生成 """
        data = json.dumps({
            "model": model,
            "prompt": data,
            "stream": stream,
        })
        return self._post("/api/generate", data, callback, stream)

    def chat(
            self,
            model: str, messages: list[dict], tools: list[dict] = None,
            callback: Callable[[Any], None] = None, stream: bool = True
    ) -> Any:
        """ 聊天 """
        if stream and callback is None: return False
        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }
        if tools:
            data["tools"] = tools
            pass
        messages = json.dumps(data)
        return self._post("/api/chat", messages, callback, stream)

    pass
