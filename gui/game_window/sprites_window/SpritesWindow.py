import pygame

from libs.c_pyqt5.tool import timer
from libs.c_pyqt5.window import GraphicsTransWindow
from app_work.game_work.sprite import SpriteAbs


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

    def add_sprite(self, sprite: SpriteAbs):
        sprite.keys_pressed = self.keys_pressed
        self.sprites.add(sprite)
        self.scene.addItem(sprite)
        self.scene.addItem(sprite.transition_item)
        self.scene.addItem(sprite.effect_item)
        pass

    def clear_sprites(self):
        self._to_clear_sprites = True
        pass

    def game_loop(self):
        # scene_rect = self.scene.sceneRect()
        if self._to_clear_sprites:
            for sprite in self.sprites:
                self.scene.removeItem(sprite)
                self.scene.removeItem(sprite.transition_item)
                self.scene.removeItem(sprite.effect_item)
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

    def hideEvent(self, a0):
        super().hideEvent(a0)
        timer.out_disconnect(self.game_loop)
        pass

    def closeEvent(self, a0):
        super().closeEvent(a0)
        timer.out_disconnect(self.game_loop)
        pass

    pass
