from abc import abstractmethod

from .Hornet_anim_maps import *
from ..HollowKnightSpriteAbs import HollowKnightSpriteAbs


class HornetSpriteAbs(HollowKnightSpriteAbs):

    def __init__(
            self,
            sprite_name: str, setup_ani_state: str,
            resources_root: str, global_size: tuple[int, int]
    ):
        super().__init__(sprite_name, setup_ani_state, resources_root, global_size)
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
        # 过渡动画
        if self.flip_x_changed:
            if self.animation_state in transition_turn_anim_map:
                self._set_transition_anim(HornetAniStatus.Turn)
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

    def run_move(self):
        if self.flip_x:
            self.sprite_x += 10
        else:
            self.sprite_x -= 10
            pass
        pass

    def up_move(self):
        self.sprite_y -= 10
        pass

    def down_move(self):
        self.sprite_y += 13
        pass

    def idle(self):
        self.switch_animation(HornetAniStatus.Idle)

    def left_run(self):
        self._set_flip_x(False)
        if self.is_transitioning(): return
        self.run_move()
        self.switch_animation(HornetAniStatus.Run)
        pass

    def right_run(self):
        self._set_flip_x(True)
        if self.is_transitioning(): return
        self.run_move()
        self.switch_animation(HornetAniStatus.Run)
        pass

    def jump(self):
        self.switch_animation(HornetAniStatus.Jump)
        pass

    pass
