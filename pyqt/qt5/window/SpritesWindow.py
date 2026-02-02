import pygame

from sprite import SpriteAbs
from sprite.hollow_knight import KnightSprite, HornetSprite
from util.pyqt_util import timer
from .base import GraphicsTransWindow


class SpritesWindow(GraphicsTransWindow):

    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__(x, y, w, h)

        self.keys_pressed: set[int] = set()
        """ 按下的键集合 """

        self.sprites: set[SpriteAbs] = set()
        """ 精灵集合 """

        self._to_clear_sprites: bool = False
        """ 是否删除所有精灵 """
        pass

    def _add_sprite(self, sprite: SpriteAbs):
        sprite.keys_pressed = self.keys_pressed
        self.sprites.add(sprite)
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

    def clear_sprites(self):
        self._to_clear_sprites = True
        pass

    def game_loop(self):
        # scene_rect = self.scene.sceneRect()
        if self._to_clear_sprites:
            for sprite in self.sprites:
                self.scene.removeItem(sprite)
                pass
            self.sprites.clear()
            self._to_clear_sprites = False
            pass

        # 更新所有精灵
        for sprite in self.sprites:
            sprite.update_anim(pygame.time.get_ticks())
            sprite.sprite_behavior_handle()
            pass

        pass

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())
        pass

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat(): return
        self.keys_pressed.discard(event.key())
        pass

    def focusOutEvent(self, event):
        # 窗口丢失焦点后清空 按键按下的记录列表
        self.keys_pressed.clear()
        pass

    def showEvent(self, event):
        super().showEvent(event)
        timer.out_connect(self.game_loop)
        pass

    def closeEvent(self, a0):
        super().closeEvent(a0)
        timer.out_disconnect(self.game_loop)
        pass

    pass
