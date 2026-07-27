from dataclasses import dataclass
from functools import partial

from app_work.game_work.sprite import KnightSprite, HornetSprite
from app_work.game_work.sprite import SpriteAbs
from .SpritesWindow import SpritesWindow

window: SpritesWindow | None = None
""" 精灵窗口 """


def create_window() -> SpritesWindow:
    global window
    if window: return window
    window = SpritesWindow()
    window.show()
    return window


def toggle_visibility():
    global window
    if window:
        if window.isVisible():
            window.hide()
        else:
            window.show()
    else:
        create_window()
    pass


@dataclass
class Sprites:
    Hornet = 'Hornet'
    KNight = 'KNight'
    pass


def create_sprite(sprite: Sprites):
    w = create_window()
    if sprite is Sprites.KNight:
        sprite = KnightSprite(w)
    elif sprite is Sprites.Hornet:
        sprite = HornetSprite(w)

    if isinstance(sprite, SpriteAbs):
        w.add_sprite(sprite)
        pass
    pass


def clear_sprites():
    create_window().clear_sprites()
    pass


menu_config = {
    '显示/隐藏': toggle_visibility,
    '添加一只小骑士': partial(create_sprite, sprite=Sprites.KNight),
    '添加一只大黄蜂': partial(create_sprite, sprite=Sprites.Hornet),
    '清除所有精灵': clear_sprites,
}
