from typing import Callable, Any

from libs.ollama_ai import OllamaAI, TagsResp

ai_api = OllamaAI()


def get_models() -> list[str]:
    tags = ai_api.tags()
    return [model.name for model in TagsResp(tags).models]


def chat_with_ai(
        message: list[dict],
        callback: Callable[[Any], None],
        finished_callback: Callable[[], None]
):
    ai_api.chat(message, callback)
    finished_callback()
    pass
