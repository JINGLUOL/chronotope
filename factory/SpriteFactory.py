from pygame.sprite import Group

from pygame_manager import screen
from sprite.hollow_knight import KnightSprite
from sprite.hollow_knight import HornetSprite


class SpriteFactory(object):

    def __init__(self):
        self.group = Group()

        self.create_hornet_sprite()
        self.create_knight_sprite()

        self.sprites_update()
        pass

    def create_knight_sprite(self):
        self.group.add(KnightSprite())
        pass

    def create_hornet_sprite(self):
        self.group.add(HornetSprite())
        pass

    def sprites_update(self):
        self.group.draw(screen)
        self.group.update()
        pass

    pass
