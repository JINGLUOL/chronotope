import threading
from functools import partial
from typing import Any, Callable

from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from app_work.tool_work.ai_window_work import ChatWidgetMessage as Message
from app_work.tool_work.ai_window_work.api import chat_with_ai, ai_api
from libs.c_pyqt5.window import TransparentWindow
from libs.ollama_ai import ChatResp
from .components import MessageSender
from .components.chat_list import ChatWidget


class AIWindow(TransparentWindow):
    update_message_finished_signal = pyqtSignal(str)

    def __init__(self):
        super(AIWindow, self).__init__(0, 0, 833, 1333)

        self.messages = []
        ''' 已加载的消息列表 '''
        self.ai_message: list[str] = []
        ''' 存储的AI回复 '''
        self.ai_message_max_len = 99
        ''' 存储AI回复最大长度 '''
        self.fps: int = 60
        ''' 更新AI回复的频率 '''

        self.update_timer = QTimer()
        ''' 更新AI回复的对象 '''
        self.update_timer.timeout.connect(self._update_message_widget)

        self.chat = ChatWidget(self)
        ''' 消息窗口 '''
        self.sender = MessageSender(self)
        ''' 发送消息的窗口 '''
        self.sender.send_signal.connect(self.send_message)

        self.layout.addWidget(self.chat, 9)
        self.layout.addWidget(self.sender, 1)

        self.drag_pos = None
        ''' 拖动窗口的缓存相对坐标 '''
        pass

    def _update_message(self, message: Any):
        """ 更新AI答复到缓存列表 """
        resp = ChatResp(message)
        self.ai_message.append(resp.message.content)
        if len(self.ai_message) % self.ai_message_max_len == 0:
            ai_message = ''.join(self.ai_message)
            self.ai_message.clear()
            self.ai_message.append(ai_message)
            pass
        pass

    def _update_message_widget(self):
        """ 更新AI答复到消息窗口 """
        self.chat.update_message_slot.emit(
            Message(''.join(self.ai_message))
        )
        pass

    def _update_message_finished(self, callback: Callable[[str], None]):
        """ AI结束答复的回调 """
        self.update_timer.stop()
        message = ''.join(self.ai_message)
        self.chat.update_message_slot.emit(Message(message))
        self.update_message_finished_signal.emit(message)
        self.ai_message.clear()
        if callback is not None: callback(message)
        pass

    def send_message(self, text: str, callback: Callable[[str], None]=None):
        if self.update_timer.isActive(): return

        self.sender.message.clear()
        message = Message(text, is_self=True)
        self.messages.append({
            "role": "user",
            "content": text
        })

        self.chat.add_message(message)

        ai_api.model = self.sender.model_list.currentText()
        self.chat.add_message(Message(''))

        self.update_timer.setInterval(int(1000 / self.fps))  # 设置AI回复更新到组件的频率
        self.update_timer.start()

        threading.Thread(
            target=chat_with_ai,
            args=[
                self.messages, self._update_message,
                partial(self._update_message_finished, callback)
            ]
        ).start()
        pass

    def hear(self):
        # audio_path = resources.output_data("user_audio.wav")
        # vosk = VoskRecognizer(resources.VoskSmallCNModel, audio_path)
        # vosk.recognize()
        # print(WhisperRecognizer('large-v3').audio_to_text(audio_path))
        pass

    def mousePressEvent(self, a0):
        if a0.button() != Qt.LeftButton: return

        self.drag_pos = a0.globalPos() - self.frameGeometry().topLeft()
        pass

    def mouseMoveEvent(self, a0):
        if self.drag_pos: self.move(a0.globalPos() - self.drag_pos)
        pass

    def mouseReleaseEvent(self, a0):
        self.drag_pos = None
        pass

    pass
