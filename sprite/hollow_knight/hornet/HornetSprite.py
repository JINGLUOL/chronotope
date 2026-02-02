from PyQt5.QtCore import Qt

from global_manager import config, resources
from .HornetSpriteAbs import HornetSpriteAbs
from .Hornet_anim_maps import wait_status, HornetAniStatus


class HornetSprite(HornetSpriteAbs):

    def __init__(self):
        super().__init__(
            'Hornet', HornetAniStatus.Stop_Somebody,
            resources.Hornet, (381, 249)
        )

        self._set_transition_anim(HornetAniStatus.Stop_Somebody)
        self._set_transition_anim(HornetAniStatus.Stop_Somebody_End)
        pass

    def _sprite_idle_handle(self):
        self.idle()
        pass

    def _sprite_call_handle(self):
        if Qt.Key_K in self.keys_pressed:
            self.jump()
            if self.is_transitioning(): return
            if self.animation.in_loop:
                if Qt.Key_S in self.keys_pressed:
                    self.down_move()
                else:
                    self.up_move()
                if Qt.Key_A in self.keys_pressed:
                    self._set_flip_x(False)
                    self.run_move()
                elif Qt.Key_D in self.keys_pressed:
                    self._set_flip_x(True)
                    self.run_move()
            else:
                self.up_move()
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
            self.idle()
            pass
        # 需要移动的行为块
        else:
            top, bottom, left, right = plus_rect.point_directions(x, y)
            if top:
                self.jump()
                if self.is_transitioning(): return
                self.up_move()
                if self.animation.in_loop:
                    if left:
                        self._set_flip_x(False)
                        self.run_move()
                    elif right:
                        self._set_flip_x(True)
                        self.run_move()
                        pass
                    pass
                pass
            elif bottom:
                self.jump()
                if self.is_transitioning(): return
                if self.animation.in_loop:
                    self.down_move()
                    if left:
                        self._set_flip_x(False)
                        self.run_move()
                    elif right:
                        self._set_flip_x(True)
                        self.run_move()
                        pass
                    pass
                else:
                    self.up_move()
                pass
            elif left:
                self.left_run()
            elif right:
                self.right_run()
            pass

        pass

    pass
