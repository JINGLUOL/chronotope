import random
from dataclasses import dataclass

import pygame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QFont, QPen

from pyqt.qt5.components import GraphicsTextRectItem
from util.pyqt_util import create_gradient_pixmap, timer
from .PianoKey import PianoKey, keyboard_map
from .PianoSound import PianoSound
from ..base.GraphicsTransWindow import GraphicsTransWindow


@dataclass
class PlayModel:
    NORMAL: str = '经典模式'
    PRACTICE: str = '练习模式'
    pass


@dataclass
class PracticeLevel:
    NONE: str = '无'
    EASY: str = '简单'
    NORMAL: str = '正常'
    HARD: str = '困难'
    HELL: str = '地狱'
    pass


# 玫瑰金 (183, 110, 121)
# 金属金 (212, 175, 55)
# 古金色 (207, 181, 59)
# 暗金色 (184, 134, 11)
# 亮金色 (255, 223, 0)
class PianoWindow(GraphicsTransWindow):

    def __init__(self, x: int, y: int, w: int, h: int, octaves: int = 3):
        super().__init__(x, y, w, h)

        self.key_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.white_key_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

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
        self.future_piano_sounds: list[str] = []
        self.current_piano_sounds: set[str] = set()
        self.destroy_piano_sounds: set[str] = set()

        # 键盘按下的按键列表
        self.keyboard_press_list: set[int] = set()

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

        # 初始化琴键
        self._init_piano_keys()

        # 钢琴面板
        self.play_model = PlayModel.NORMAL
        self.player_t_score: int = 0
        self.player_f_score: int = 0
        self.panel = self._init_piano_panel()

        # 练习项列表
        self.practice_items: set[GraphicsTextRectItem] = set()
        self.sorted_practice_items: list[GraphicsTextRectItem] = []
        self.practice_level: str = PracticeLevel.NONE
        self.practice_item_speed: int = 7
        self.practice_item_pen: QPen = QPen(Qt.NoPen)
        self.practice_first_item_pen: QPen = QPen(QColor(255, 0, 0), 5)
        self.practice_item_list_len: int = 0

        # 更新面板
        self.update_panel()
        pass

    def _init_piano_panel(self) -> GraphicsTextRectItem:
        width = self.white_key_w * 10
        height = 30
        x = int((self.width() - width) / 2)
        y = self.height() - self.white_key_h - height

        # 初始化面板的背景
        gradient = QLinearGradient(0, 0, width, 0)
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.05, QColor(255, 255, 255, 99))
        gradient.setColorAt(0.5, QColor(255, 223, 0))
        gradient.setColorAt(0.95, QColor(255, 255, 255, 99))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))

        panel = GraphicsTextRectItem(self.scene, width, height, QColor(0, 0, 0), gradient)
        panel.set_pen(QPen(Qt.NoPen))

        # 初始化面板
        panel.set_pos(x, y)
        return panel

    def _init_piano_keys(self):
        # 中央C在标准钢琴八度的位置
        c_pos = 4
        # 中央C的MIDI编号
        c_code = 60
        # 起始八度
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
            self.key_notes[len(self.key_notes) - 3:]
        )
        # 创建每个八度
        start_x += self.white_key_w * 2
        for octave in range(start_octave, start_octave + self.octaves):
            self._init_piano_keys_by_notes(octave, start_midi, start_x, start_y, self.key_notes)
            start_x += self.white_key_w * 7
            start_midi += 12
            pass
        # 额外高音
        self._init_piano_keys_by_notes(
            start_octave + self.octaves, start_midi, start_x, start_y,
            self.key_notes[:1]
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
        pass

    def update_panel(self):
        self.panel.set_text(
            f"模式：{self.play_model} 难度：{self.practice_level} 对：{self.player_t_score} 错：{self.player_f_score}"
        )
        pass

    def set_practice_difficulty(self, difficulty):
        if difficulty is PracticeLevel.NONE:
            self.play_model = PlayModel.NORMAL
            self.practice_item_list_len = 0
            self.practice_item_speed = 23
        elif difficulty is PracticeLevel.EASY:
            self.play_model = PlayModel.PRACTICE
            self.practice_item_list_len = 3
            self.practice_item_speed = 1
        elif difficulty is PracticeLevel.NORMAL:
            self.play_model = PlayModel.PRACTICE
            self.practice_item_list_len = 7
            self.practice_item_speed = 2
        elif difficulty is PracticeLevel.HARD:
            self.play_model = PlayModel.PRACTICE
            self.practice_item_list_len = 11
            self.practice_item_speed = 3
        elif difficulty is PracticeLevel.HELL:
            self.play_model = PlayModel.PRACTICE
            self.practice_item_list_len = 13
            self.practice_item_speed = 7
            pass
        self.practice_level = difficulty
        self.player_t_score = 0
        self.player_f_score = 0

        # 填充练习列表
        if len(self.practice_items) < self.practice_item_list_len:
            for i in range(len(self.practice_items), self.practice_item_list_len):
                item: GraphicsTextRectItem = GraphicsTextRectItem(self.scene, 50, 50)
                item.set_font(QFont('Arial', 17, QFont.Bold))
                item.set_z_value(-1)
                self.practice_items.add(item)
                self.practice_item_reset(item)
                pass
            pass

        self.update_panel()
        pass

    def practice_item_reset(self, item: GraphicsTextRectItem):
        item.set_pen(self.practice_item_pen)
        item.set_text(self.white_key_notes[int(random.random() * len(self.white_key_notes))])
        item.set_pos(
            random.random() * (self.width() - 198) + 99,
            random.random() * 198 - 99
        )
        self.sorted_practice_items = sorted(self.practice_items, key=lambda obj: obj.y(), reverse=True)
        pass

    def press_event(self, key_name: str):
        if self.l_pedal:
            velocity = 50  # 柔音力度
            sustain = -300
            pass
        elif self.r_pedal:
            velocity = 127  # 最大力度
            sustain = 300
            pass
        else:
            velocity = 100  # 正常力度
            sustain = 0
            pass
        self.piano_sounds_map[key_name].play(pygame.time.get_ticks(), velocity, sustain)
        self.future_piano_sounds.append(key_name)
        pass

    def release_event(self, key_name: str):
        self.piano_sounds_map[key_name].set_stop_time(pygame.time.get_ticks())
        pass

    def play_piano(self):
        current_time = pygame.time.get_ticks()

        if len(self.sorted_practice_items) > 0:
            self.sorted_practice_items[0].set_pen(self.practice_first_item_pen)
            pass

        discarded_practice_items = set()
        fps_len = len(self.future_piano_sounds)
        for index, item in enumerate(self.sorted_practice_items):
            if item.y() + self.white_key_h + 50 < self.height():
                item.move(0, self.practice_item_speed)
                if index < fps_len:
                    if self.future_piano_sounds[index][:-1] == item.get_text():
                        self.player_t_score += 1
                        self.practice_item_reset(item)
                    else:
                        self.player_f_score += 1
                        self.practice_item_reset(item)
                    pass
                pass
            else:
                if len(self.practice_items) > self.practice_item_list_len:
                    discarded_practice_items.add(item)
                    item.remove()
                    pass
                else:
                    self.player_f_score += 1
                    self.practice_item_reset(item)
                    pass
                pass
            pass
        self.practice_items.difference_update(discarded_practice_items)
        self.update_panel()

        self.current_piano_sounds.update(self.future_piano_sounds)
        self.future_piano_sounds.clear()
        self.current_piano_sounds.difference_update(self.destroy_piano_sounds)
        self.destroy_piano_sounds.clear()
        for sound_key in self.current_piano_sounds:
            if self.piano_sounds_map[sound_key].terminate(current_time):
                self.destroy_piano_sounds.add(sound_key)
                pass
            pass

        pass

    def focusOutEvent(self, event):
        # 窗口丢失焦点后清空 按键按下的记录列表
        self.keyboard_press_list.clear()
        pass

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() in self.keyboard_press_list: return
        self.keyboard_press_list.add(event.key())
        if event.key() in keyboard_map:
            self.press_event(keyboard_map[event.key()])
            pass
        pass

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat(): return
        self.keyboard_press_list.discard(event.key())
        if event.key() in keyboard_map:
            self.release_event(keyboard_map[event.key()])
            pass
        pass

    def showEvent(self, event):
        super().showEvent(event)
        timer.out_connect(self.play_piano)
        pass

    def hideEvent(self, a0):
        super().hideEvent(a0)
        timer.out_disconnect(self.play_piano)
        pass

    def closeEvent(self, a0):
        super().closeEvent(a0)
        timer.out_disconnect(self.play_piano)
        pass

    def destroy(self, d_win=..., d_sub_wins=...):
        super().destroy(d_win, d_sub_wins)
        timer.out_disconnect(self.play_piano)
        pass

    pass
