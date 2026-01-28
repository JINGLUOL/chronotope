import pygame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QLinearGradient

from util.pyqt_util import create_gradient_pixmap
from .PianoKey import PianoKey
from .PianoSound import PianoSound
from ..base.GraphicsTransWindow import GraphicsTransWindow


# 玫瑰金 (183, 110, 121)
# 金属金 (212, 175, 55)
# 古金色 (207, 181, 59)
# 暗金色 (184, 134, 11)
# 亮金色 (255, 223, 0)
class PianoWindow(GraphicsTransWindow):

    def __init__(self, x: int, y: int, w: int, h: int, octaves: int = 3):
        super().__init__(x, y, w, h)

        # 踏板
        self.l_pedal: bool = False
        """ 弱音踏板 / 柔音踏板 """
        self.c_pedal: bool = False
        """ 特定延音踏板 / 消音踏板 """
        self.r_pedal: bool = False
        """ 延音踏板 / 制音踏板 """

        # 八度总数
        self.octaves: int = max(min(7, octaves), 1)

        # 钢琴键列表
        self.piano_sounds_map: dict[str, PianoSound] = {}
        self.piano_sounds: list[PianoSound] = []

        # 白键宽高
        self.white_key_w: int = 60
        self.white_key_h: int = 333

        # 黑键宽高
        self.black_key_w: int = int(self.white_key_w / 2)
        self.black_key_h: int = int(self.white_key_h * 3 / 4)

        # 白键渐变色
        self.white_key_gradient = QLinearGradient(0, 0, 0, self.white_key_h)
        self.white_key_gradient.setColorAt(0, QColor(255, 255, 255, 99))
        self.white_key_gradient.setColorAt(0.7, QColor(255, 255, 255))
        self.white_key_gradient.setColorAt(1, QColor(0xD7EEF8))

        # 白键边框渐变色
        self.white_key_border_gradient = QLinearGradient(0, 0, 0, self.white_key_h)
        self.white_key_border_gradient.setColorAt(0, QColor(255, 255, 255))
        self.white_key_border_gradient.setColorAt(0.5, QColor(0xD7EEF8))
        self.white_key_border_gradient.setColorAt(1, QColor(255, 223, 0))

        # 黑键渐变色
        self.black_key_gradient = QLinearGradient(0, 0, 0, self.black_key_h)
        self.black_key_gradient.setColorAt(0, QColor(0, 0, 0, 99))
        self.black_key_gradient.setColorAt(0.7, QColor(0, 0, 0))
        self.black_key_gradient.setColorAt(1, QColor(183, 110, 121))

        # 黑键边框渐变色
        self.black_key_border_gradient = QLinearGradient(0, 0, 0, self.black_key_h)
        self.black_key_border_gradient.setColorAt(0, QColor(0, 0, 0))
        self.black_key_border_gradient.setColorAt(0.8, QColor(184, 134, 11))  # 暗金色
        self.black_key_border_gradient.setColorAt(1, QColor(255, 223, 0))  # 亮金色

        # 音检索
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_piano)
        self.timer.setInterval(16)  # 60FPS

        self._init_piano_keys()
        pass

    def _init_piano_keys(self):
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        c_pos = 4
        c_code = 60
        start_octave = c_pos - int(self.octaves / 2)
        if self.octaves % 2 == 0:
            start_octave += 1
            pass
        # 起始八度
        start_octave = max(min(start_octave, c_pos), 1)
        # 起始编号
        start_midi = c_code - (c_pos - start_octave) * 12

        # 绘制起始位置
        start_x = max((self.width() - (self.octaves * 7 + 3) * self.white_key_w) / 2, 0)
        start_y = self.height() - self.white_key_h
        # 额外低音
        self._init_piano_keys_by_notes(
            start_octave - 1, start_midi - 3, start_x, start_y,
            notes[len(notes) - 3:]
        )
        # 创建每个八度
        start_x += self.white_key_w * 2
        for octave in range(start_octave, start_octave + self.octaves):
            self._init_piano_keys_by_notes(octave, start_midi, start_x, start_y, notes)
            start_x += self.white_key_w * 7
            start_midi += 12
            pass
        # 额外高音
        self._init_piano_keys_by_notes(
            start_octave + self.octaves, start_midi, start_x, start_y,
            [notes[0]]
        )
        pass

    def _init_piano_keys_by_notes(
            self,
            octave: int, start_midi: int,
            start_x, start_y, notes: list[str]
    ):
        # 根据一个八度序列初始化
        white_key_n = 0
        for i, note in enumerate(notes):
            key_name = f"{note}{octave}"
            key_midi = start_midi + i

            if '#' in note:
                piano_key: PianoKey = PianoKey(
                    key_name, key_midi,
                    create_gradient_pixmap(
                        self.black_key_w, self.black_key_h,
                        self.black_key_gradient, Qt.AlignCenter,
                        key_name, 9, True, Qt.white
                    ),
                    self.black_key_border_gradient, 3
                )
                self.scene.addItem(piano_key)
                piano_key.setPos(start_x + self.white_key_w * white_key_n - self.black_key_w / 2, start_y)
                piano_key.setZValue(1)
                pass
            else:
                piano_key: PianoKey = PianoKey(
                    key_name, key_midi,
                    create_gradient_pixmap(
                        self.white_key_w, self.white_key_h,
                        self.white_key_gradient, Qt.AlignCenter | Qt.AlignBottom,
                        key_name, 9, True, Qt.black
                    ),
                    self.white_key_border_gradient, 3
                )
                self.scene.addItem(piano_key)
                piano_key.setPos(start_x + self.white_key_w * white_key_n, start_y)
                piano_key.setZValue(0)
                white_key_n += 1
                pass
            piano_key.signals.press_signal.connect(self.press_event)
            piano_key.signals.release_signal.connect(self.release_event)
            self.piano_sounds_map[key_name] = PianoSound(key_midi)
            pass
        self.piano_sounds.extend(self.piano_sounds_map.values())
        pass

    def press_event(self, key_name: str):
        if self.l_pedal:
            velocity = 50  # 柔音力度
            pass
        elif self.r_pedal:
            velocity = 127  # 正常力度
            pass
        else:
            velocity = 100  # 正常力度
            pass
        self.piano_sounds_map[key_name].play(pygame.time.get_ticks(), velocity)
        pass

    def release_event(self, key_name: str):
        self.piano_sounds_map[key_name].set_stop_time(pygame.time.get_ticks())
        pass

    def play_piano(self):
        current_time = pygame.time.get_ticks()
        for piano_sound in self.piano_sounds:
            piano_sound.terminate(current_time)
            pass
        pass

    def showEvent(self, event):
        super().showEvent(event)
        self.timer.start()
        pass

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.timer.stop()
        pass

    pass
