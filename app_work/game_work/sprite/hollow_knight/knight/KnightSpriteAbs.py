from abc import abstractmethod

from PyQt5.QtWidgets import QWidget

from .Knight_anim_maps import *
from ..HollowKnightSpriteAbs import HollowKnightSpriteAbs


class KnightSpriteAbs(HollowKnightSpriteAbs):

    def __init__(
            self,
            sprite_name: str, setup_ani_state: str,
            resources_root: str, parent: QWidget,
    ):
        super().__init__(sprite_name, setup_ani_state, resources_root, parent)
        pass

    @abstractmethod
    def _sprite_idle_handle(self):
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
                (self.is_transitioning() or state is self.animation_state)
        ):
            return
        # 连贯动画
        if self.animation_state in coherent_anim_map and state is coherent_anim_map[self.animation_state]:
            self._set_anim(state)
            return
        # 过渡动画
        if self.flip_x_changed:
            if self.animation_state in turn_transition_anim_map:
                self._set_transition_anim(KnightAniStatus.Turn)
            self.flip_x_changed = False
            return
        elif state in before_anim_transition_map:
            self._set_transition_anim(before_anim_transition_map[state])
            pass
        elif self.animation_state in after_anim_transition_map:
            self._set_transition_anim(after_anim_transition_map[self.animation_state])
            pass

        # 下一个动画
        self._set_anim(state)
        pass

    def walk_move(self):
        if not self.isVisible(): return
        if self.flip_x:
            self.sprite_x += 3
        else:
            self.sprite_x -= 3
        pass

    def run_move(self):
        if not self.isVisible() and KnightAniStatus.Shadow_Recharge not in self.transition_anim_set: return
        if self.flip_x:
            self.sprite_x += 7
        else:
            self.sprite_x -= 7
        pass

    def up_move(self):
        if not self.isVisible(): return
        self.sprite_y -= 7

    def down_move(self):
        if not self.isVisible(): return
        self.sprite_y += 13

    def idle(self):
        self.switch_animation(KnightAniStatus.IDLE)
        pass

    def idle_wind(self):
        self.switch_animation(KnightAniStatus.IDLE_WIND)
        pass

    def left_walk(self):
        self._set_flip_x(False)
        self.walk_move()
        self.switch_animation(KnightAniStatus.WALK)
        pass

    def right_walk(self):
        self._set_flip_x(True)
        self.walk_move()
        self.switch_animation(KnightAniStatus.WALK)
        pass

    def left_run(self):
        self._set_flip_x(False)
        self.run_move()
        self.switch_animation(KnightAniStatus.RUN)
        pass

    def right_run(self):
        self._set_flip_x(True)
        self.run_move()
        self.switch_animation(KnightAniStatus.RUN)
        pass

    def jump(self):
        self.up_move()
        self.switch_animation(KnightAniStatus.Airborne)
        pass

    def down(self):
        if self.animation_state is KnightAniStatus.Fall: self.down_move()
        self.switch_animation(KnightAniStatus.Fall)
        pass

    def look_up(self):
        self.switch_animation(KnightAniStatus.LookUp)
        pass

    def look_down(self):
        self.switch_animation(KnightAniStatus.LookDown)
        pass

    def reach_out(self):
        self.switch_animation(KnightAniStatus.Reach_Out)
        pass

    def to_shadow(self):
        if KnightAniStatus.Shadow_Recharge in self.transition_anim_set: return
        self._set_transition_anim(KnightAniStatus.Shadow_Recharge)
        pass

    pass
