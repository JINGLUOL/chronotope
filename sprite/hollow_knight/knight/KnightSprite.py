from PyQt5.QtCore import Qt

from global_manager import config, resources, screen
from .KnightSpriteAbs import KnightSpriteAbs
from .Knight_anim_maps import wait_status


class KnightSprite(KnightSpriteAbs):

    def __init__(self):
        super().__init__("Knight", resources.Knight)
        pass

    def _sprite_idle_handle(self):
        self.idle()
        pass

    def _sprite_call_handle(self):
        if Qt.Key_K in self.keys_pressed:
            if Qt.Key_S in self.keys_pressed:
                self.down()
            else:
                self.up()
            if self.animation.in_loop:
                if Qt.Key_A in self.keys_pressed:
                    self._set_flip_x(False)
                    self.walk_move()
                elif Qt.Key_D in self.keys_pressed:
                    self._set_flip_x(True)
                    self.walk_move()
        elif Qt.Key_A in self.keys_pressed:
            self.left_run()
        elif Qt.Key_D in self.keys_pressed:
            self.right_run()
        else:
            self.idle()
            pass

        pass

    def _sprite_follow_handle(self):
        # 获取鼠标坐标
        x = config.mouse_x - self.sprite_x
        y = config.mouse_y - self.sprite_y

        plus_rect = self.animation.current_rect + \
                    (
                            self.animation_state in wait_status and
                            self.follow_pass_range or
                            self.follow_space_range
                    )

        # 无需移动的行为块
        if plus_rect.include(x, y):
            top, bottom, left, right = self.animation.current_rect.point_directions(x, y)
            if left:
                self._set_flip_x(False)
            elif right:
                self._set_flip_x(True)
            if top:
                self.look_up()
            elif bottom:
                self.look_down()
            else:
                if self.sprite_y < screen.get_height() / 2:
                    self.idle_wind()
                else:
                    self.idle()
                pass
            pass
        # 需要移动的行为块
        else:
            # print('精灵矩形', repr(self.animation.current_rect))
            # print('增值矩形', repr(plus_rect))
            # print('坐标差值', x, y)
            # print('当前坐标', self.x(), self.y())
            # print('鼠标坐标', config.mouse_x, config.mouse_y)
            top, bottom, left, right = plus_rect.point_directions(x, y)
            if top:
                self.up()
                if self.animation.in_loop:
                    if left:
                        self._set_flip_x(False)
                        self.walk_move()
                    elif right:
                        self._set_flip_x(True)
                        self.walk_move()
                        pass
                    pass
                pass
            elif bottom:
                self.down()
                if self.animation.in_loop:
                    if left:
                        self._set_flip_x(False)
                        self.walk_move()
                    elif right:
                        self._set_flip_x(True)
                        self.walk_move()
                        pass
                    pass
                pass
            elif left:
                self.left_walk()
            elif right:
                self.right_walk()
            pass

        pass

    pass
