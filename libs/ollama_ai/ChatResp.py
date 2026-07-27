from . import ToolCall
from ..jing_luo.json import JSONObject


class ChatMessage(JSONObject):
    role = None
    ''' 角色 '''
    content = None
    ''' 回复内容 '''
    thinking = None
    ''' 思考内容 '''
    tool_calls: list[ToolCall] = None
    ''' 工具调用 '''
    images = None
    ''' ？ '''

    def __init__(self, data):
        super().__init__(data)

        if self.tool_calls: self.tool_calls = [ToolCall(tool_call) for tool_call in self.tool_calls]
        pass

    pass


class ChatResp(JSONObject):
    model = None
    ''' 使用的模型 '''
    created_at = None
    message: ChatMessage | dict = None
    ''' 模型回复信息对象 '''
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
        super().__init__(data)

        if self.message: self.message = ChatMessage(self.message)
        pass

    pass
