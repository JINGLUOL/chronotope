import json
import wave
from dataclasses import dataclass
from datetime import datetime

import pyaudio
from vosk import Model, KaldiRecognizer


@dataclass
class AudioSegment:
    """音频片段数据类"""
    data: bytes
    start_time: datetime
    end_time: datetime
    text: str = ""
    filename: str = ""
    sample_rate: int = 16000
    sample_width: int = 2  # 16-bit = 2 bytes
    pass


class VoskRecognizer:

    def __init__(self, model_path: str, file_path, sample_rate: int = AudioSegment.sample_rate, chunk_size: int = 4000):
        # 定义采样参数
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size

        # 加载模型
        self.model = Model(model_path)  # 模型路径
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

        self.current_segment = AudioSegment(data=b"", start_time=datetime.now(), end_time=datetime.now())
        self.current_segment.filename = file_path

        # 定义结束语
        # self.end_str_map: set[str] = {'就这些', }
        # 定义识别无效结束次数
        self.lost_num_max: int = 23
        # 定义识别无效结束当前次数
        self.lost_current_num: int = 0
        pass

    def recognize(self):
        # 初始化音频流
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        try:
            while True:
                data = stream.read(self.chunk_size)
                self.current_segment.data += data

                if self.recognizer.AcceptWaveform(data):
                    self.lost_current_num -= self.lost_current_num
                    # result = json.loads(self.recognizer.Result())['text'].strip().replace(' ', '')
                    # if True in [result.endswith(end_str) for end_str in self.end_str_map]: break
                else:
                    self.lost_current_num += 1
                    if self.lost_current_num >= self.lost_num_max: break
                    pass
        except KeyboardInterrupt:
            print("录音已终止")
        finally:
            # 清理资源
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("录音记录中...")
        self._finalize_segment()
        pass

    def _finalize_segment(self):
        # 设置结束事件
        self.current_segment.end_time = datetime.now()

        # 保存音频文件
        if not self.current_segment.data: return

        # 保存WAV文件
        with wave.open(self.current_segment.filename, "wb") as wf:
            wf.setnchannels(1)  # 单声道
            wf.setsampwidth(self.current_segment.sample_width)
            wf.setframerate(self.sample_rate)
            wf.writeframes(self.current_segment.data)
            pass

        self.current_segment.data = b""
        self.current_segment.start_time = datetime.now()
        self.current_segment.end_time = datetime.now()
        self.lost_current_num -= self.lost_current_num
        print('已记录一段录音')
        pass

    pass
