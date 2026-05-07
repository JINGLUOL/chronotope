import threading
from typing import Any

from PyQt5.QtCore import Qt

from app_work.tool_work.ai_window_work import ChatWidgetMessage as Message
from app_work.tool_work.ai_window_work.api import chat_with_ai, ai_api
from libs.c_pyqt5.window import TransparentWindow
from libs.ollama_ai import ChatResp
from .components import MessageSender
from .components.chat_list import ChatWidget


class AIWindow(TransparentWindow):

    def __init__(self):
        super(AIWindow, self).__init__(0, 0, 833, 1333)

        self.messages = []
        self.ai_message: list[str] = []

        self.chat = ChatWidget(self)
        self.sender = MessageSender(self)
        self.layout.addWidget(self.chat, 9)
        self.layout.addWidget(self.sender, 1)

        self.sender.send_signal.connect(self.send_message)

        self.drag_pos = None
        pass

    def send_message(self, text: str):
        message = Message(text, is_self=True)
        self.messages.append({
            "role": "user",
            "content": text
        })

        self.chat.add_message(message)

        ai_api.model = self.sender.model_list.currentText()
        self.chat.add_message(Message(''))
        threading.Thread(
            target=chat_with_ai,
            args=[self.messages, self.update_message, self.ai_message.clear]
        ).start()
        pass

    def update_message(self, message: Any):
        resp = ChatResp(message)
        self.ai_message.append(resp.message.content)
        ai_message = ''.join(self.ai_message)
        if len(self.ai_message) % 99 == 0:
            self.ai_message.clear()
            self.ai_message.append(ai_message)
        self.chat.update_message_slot.emit(Message(ai_message))
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
