import pygame
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter

from .GraphicsTransparentWindow import GraphicsTransparentWindow
from sprite import SpriteAbs
from sprite.hollow_knight import KnightSprite, HornetSprite


class SpritesWindow(GraphicsTransparentWindow):

    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__(x, y, w, h)

        self.keys_pressed: set[int] = set()
        """ 按下的键集合 """

        # 精灵列表
        self.sprites: list[SpriteAbs] = []
        self.create_knight_sprite()
        self.create_hornet_sprite()

        self.delay: int = 16

        # 游戏循环
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(self.delay)  # 60FPS

        # 帧率计算
        self.frame_count = 0
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(1000)
        pass

    def _add_sprite(self, sprite: SpriteAbs):
        sprite.keys_pressed = self.keys_pressed
        self.sprites.append(sprite)
        self.scene.addItem(sprite)
        pass

    def create_knight_sprite(self):
        sprite = KnightSprite()
        self._add_sprite(sprite)
        pass

    def create_hornet_sprite(self):
        sprite = HornetSprite()
        self._add_sprite(sprite)
        pass

    def game_loop(self):
        # scene_rect = self.scene.sceneRect()

        # 更新所有精灵
        for sprite in self.sprites:
            sprite.update_anim(pygame.time.get_ticks())
            sprite.sprite_behavior_handle()

        self.frame_count += 1
        pass

    def update_fps(self):
        # print(f"FPS: {self.frame_count}")
        self.frame_count = 0
        pass

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())
        pass

    def keyReleaseEvent(self, event):
        self.keys_pressed.discard(event.key())
        pass

    def focusOutEvent(self, event):
        # 窗口丢失焦点后清空 按键按下的记录列表
        self.keys_pressed.clear()
        pass

    pass
