import pygame

from global_manager import config, resources
from pygame_manager import screen
from .KnightSpriteAbs import KnightSpriteAbs
from .Knight_anim_maps import wait_status


class KnightSprite(KnightSpriteAbs):

    def __init__(self):
        super().__init__("AKnight", resources.Knight)
        pass

    def _sprite_call_handle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_k]:
            if keys[pygame.K_s]:
                self.down()
            else:
                self.up()
            if self.animation.in_loop:
                if keys[pygame.K_a]:
                    self._set_flip_x(False)
                    self.walk_move()
                elif keys[pygame.K_d]:
                    self._set_flip_x(True)
                    self.walk_move()
        elif keys[pygame.K_a]:
            self.left_run()
        elif keys[pygame.K_d]:
            self.right_run()
        else:
            self.idle()
            pass
        pass

    def _sprite_follow_handle(self):
        # 获取鼠标坐标
        mouse_x = config.mouse_x
        mouse_y = config.mouse_y

        rect = self.animation.current_rect

        top = self.y + rect.y - mouse_y
        left = self.x + rect.x - mouse_x
        bottom = self.y + rect.h - mouse_y
        right = self.x + rect.w - mouse_x
        move_range = self.animation_state in wait_status and self.follow_pass_range or self.follow_space_range
        if max(top, left) > move_range or min(bottom, right) < -move_range:
            if top > 0:
                self.up()
                if self.animation.in_loop:
                    if left > 0:
                        self._set_flip_x(False)
                        self.walk_move()
                    elif right < 0:
                        self._set_flip_x(True)
                        self.walk_move()
                        pass
                    pass
                pass
            elif bottom < 0:
                self.down()
                if self.animation.in_loop:
                    if left > 0:
                        self._set_flip_x(False)
                        self.walk_move()
                    elif right < 0:
                        self._set_flip_x(True)
                        self.walk_move()
                        pass
                    pass
                pass
            elif left > 0:
                self.left_walk()
            elif right < 0:
                self.right_walk()
            pass
        else:
            if left > 0:
                self._set_flip_x(False)
            elif right < 0:
                self._set_flip_x(True)
            if top > 0:
                self.look_up()
            elif bottom < 0:
                self.look_down()
            else:
                if self.y < screen.get_height() / 2:
                    self.idle_wind()
                else:
                    self.idle()
                pass
            pass
        pass

    pass
