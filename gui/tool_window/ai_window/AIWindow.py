import threading
from typing import Any, Callable

from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from app_work.tool_work.ai_window_work import ChatWidgetMessage as Message
from app_work.tool_work.ai_window_work.api import chat_with_ai
from libs.c_pyqt5.window import TransparentWindow
from libs.ollama_ai import ChatResp
from .components import MessageSender
from .components.chat_list import ChatWidget


class AIWindow(TransparentWindow):
    ai_send_finished_solt = pyqtSignal()

    def __init__(self):
        super(AIWindow, self).__init__(False)
        self.setGeometry(0, 0, 833, 1333)
        self.ai_send_finished_solt.connect(self._ai_send_finished)

        self._lock = threading.Lock()
        ''' AI回复加载锁 '''
        self._msg_buffer = []
        ''' AI回复缓存列表 '''
        self._update_timer = QTimer()
        ''' AI回复更新器 '''
        self.fps: int = 30
        ''' AI回复更新器更新频率 '''
        self._ai_sending: bool = False
        ''' AI回复锁定变量 '''
        self._ai_send_finished_callback: Callable[[str], None] | None = None
        ''' AI回复结束回调 '''

        self._update_timer.timeout.connect(self._update_ai_resp)

        self.messages = []
        ''' 已加载的消息列表 '''

        self.chat = ChatWidget(self)
        ''' 消息窗口 '''
        self.sender = MessageSender(self)
        ''' 发送消息的窗口 '''
        self.sender.send_slot.connect(self.send_message)

        self.layout.addWidget(self.chat, 9)
        self.layout.addWidget(self.sender, 1)

        self.drag_pos = None
        ''' 拖动窗口的缓存相对坐标 '''
        pass

    def _buffer_ai_resp(self, message: Any):
        """ 更新AI答复到缓存列表 """
        resp = ChatResp(message)
        with self._lock:
            self._msg_buffer.append(resp.message.content)
            pass
        pass

    def _update_ai_resp(self):
        # 更新AI答复到消息窗口
        with self._lock:
            if not self._msg_buffer: return
            self.chat.update_message_slot.emit(Message(
                ''.join(self._msg_buffer),
            ))
            self._msg_buffer.clear()
            pass
        pass

    def _ai_send_finished(self):
        """ AI结束答复的回调 """
        self._update_timer.stop()
        self._update_ai_resp()

        message = self.chat.pre_bubble.msg_label.text()
        self.messages.append({
            "role": "assistant",
            "content": message
        })
        self._ai_sending = False
        callback = self._ai_send_finished_callback
        self._ai_send_finished_callback = None
        if callback is not None: callback(message)
        pass

    def send_message(self, text: str, callback: Callable[[str], None] = None):
        if self._ai_sending: return
        self._ai_send_finished_callback = callback
        self._ai_sending = True
        self._update_timer.start(int(1000 / self.fps))

        self.sender.message.clear()
        message = Message(text, is_self=True)
        self.messages.append({
            "role": "user",
            "content": text
        })

        self.chat.add_message(message)

        model = self.sender.model_list.currentText()
        self.chat.add_message(Message(''))

        threading.Thread(
            target=chat_with_ai,
            args=[
                model, self.messages,
                self._buffer_ai_resp,
                self.ai_send_finished_solt.emit
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
