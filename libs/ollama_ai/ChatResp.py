from . import ToolCall


class ChatMessage:
    role = None
    content = None
    thinking = None
    tool_calls = None
    images = None

    def __init__(self, data):
        for key, value in data.items(): setattr(self, key, value)

        if self.tool_calls:
            tool_calls = []
            for tool_call in self.tool_calls:
                tool_calls.append(ToolCall(tool_call))
                pass
            self.tool_calls = tool_calls
        pass

    pass


class ChatResp:
    model = None
    created_at = None
    message = None
    done = None
    done_reason = None
    total_duration = None
    load_duration = None
    prompt_eval_count = None
    prompt_eval_duration = None
    eval_count = None
    eval_duration = None
    logprobs = None

    def __init__(self, data):
        for key, value in data.items(): setattr(self, key, value)
        if self.message: self.message = ChatMessage(self.message)
        pass

    pass
