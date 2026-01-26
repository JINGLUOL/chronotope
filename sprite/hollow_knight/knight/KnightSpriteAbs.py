from abc import abstractmethod

from .Knight_anim_maps import *
from ..HollowKnightSpriteAbs import HollowKnightSpriteAbs


class KnightSpriteAbs(HollowKnightSpriteAbs):

    def __init__(self, sprite_name: str, resources_root: str):
        super().__init__(sprite_name, KnightAniStatus.IDLE, resources_root)
        pass

    @abstractmethod
    def _sprite_follow_handle(self):
        pass

    @abstractmethod
    def _sprite_call_handle(self):
        pass

    def switch_animation(self, state: str):
        # 过渡动画未结束 | 同动画不进行更替
        if (
                not (self.flip_x_changed or self.flip_y_changed) and
                (self.transition_ani or state is self.animation_state)
        ):
            return
        # 过渡动画
        if self.flip_x_changed:
            if self.animation_state in turn_transition_anim_map:
                self._set_transition_anim(KnightAniStatus.Turn)
            self.flip_x_changed = False
            return
        elif self.animation_state in transition_anim_map:
            self._set_transition_anim(transition_anim_map[self.animation_state])
            pass
        # 下一个动画
        self._set_anim(state)
        pass

    def walk_move(self):
        if self.flip_x:
            self.sprite_x += 3
        else:
            self.sprite_x -= 3
        pass

    def run_move(self):
        if self.flip_x:
            self.sprite_x += 7
        else:
            self.sprite_x -= 7
        pass

    def up_move(self):
        self.sprite_y -= 7

    def down_move(self):
        self.sprite_y += 13

    def idle(self):
        self.switch_animation(KnightAniStatus.IDLE)
        pass

    def idle_wind(self):
        self.switch_animation(KnightAniStatus.IDLE_WIND)
        pass

    def left_walk(self):
        self._set_flip_x(False)
        if not self.transition_ani: self.walk_move()
        self.switch_animation(KnightAniStatus.WALK)
        pass

    def right_walk(self):
        self._set_flip_x(True)
        if not self.transition_ani: self.walk_move()
        self.switch_animation(KnightAniStatus.WALK)
        pass

    def left_run(self):
        self._set_flip_x(False)
        if not self.transition_ani: self.run_move()
        self.switch_animation(KnightAniStatus.RUN)
        pass

    def right_run(self):
        self._set_flip_x(True)
        if not self.transition_ani: self.run_move()
        self.switch_animation(KnightAniStatus.RUN)
        pass

    def up(self):
        if self.animation.in_loop: self.up_move()
        self.switch_animation(KnightAniStatus.Scream)
        pass

    def down(self):
        if self.animation.in_loop: self.down_move()
        self.switch_animation(KnightAniStatus.SD_Charge_Ground)
        pass

    def look_up(self):
        self.switch_animation(KnightAniStatus.LookUp)
        pass

    def look_down(self):
        self.switch_animation(KnightAniStatus.LookDown)
        pass

    pass
