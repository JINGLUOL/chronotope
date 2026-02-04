from abc import abstractmethod

from .Hornet_anim_maps import *
from ..HollowKnightSpriteAbs import HollowKnightSpriteAbs


class HornetSpriteAbs(HollowKnightSpriteAbs):

    def __init__(
            self,
            sprite_name: str, setup_ani_state: str,
            resources_root: str
    ):
        super().__init__(sprite_name, setup_ani_state, resources_root)
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
        # 添加过渡动画
        if self.flip_x_changed:
            if self.animation_state in turn_anim_transition_map:
                self._set_transition_anim(HornetAniStatus.Turn)
                pass
            self.flip_x_changed = False
            return
        elif state in before_anim_transition_map:
            self._set_transition_anim(before_anim_transition_map[state])
            pass
        elif self.animation_state in after_anim_transition_map:
            self._set_transition_anim(after_anim_transition_map[self.animation_state])
            pass
        # 添加效果动画
        if state in effect_transition_map:
            effect_anim_name = effect_transition_map[state]
            self.effect_loop = effect_anim_name in effect_loop_map
            self._set_effect_anim(effect_anim_name)
        else:
            self.effect_anim_list.clear()
            self._remove_effect_item()
        # 下一个动画
        self._set_anim(state)
        pass

    def run_move(self):
        if not self.isVisible(): return
        if self.flip_x:
            self.sprite_x += 10
        else:
            self.sprite_x -= 10
            pass
        pass

    def up_move(self):
        if not self.isVisible(): return
        self.sprite_y -= 14
        pass

    def down_move(self):
        if not self.isVisible(): return
        self.sprite_y += 13
        pass

    def idle(self):
        self.switch_animation(HornetAniStatus.Idle)

    def left_run(self):
        self._set_flip_x(False)
        self.run_move()
        self.switch_animation(HornetAniStatus.Run)
        pass

    def right_run(self):
        self._set_flip_x(True)
        self.run_move()
        self.switch_animation(HornetAniStatus.Run)
        pass

    def jump(self):
        if not self.animation.in_loop: return
        self.up_move()
        self.switch_animation(HornetAniStatus.Jump)
        pass

    def fall(self):
        if not self.animation.in_loop: return
        self.down_move()
        self.switch_animation(HornetAniStatus.Fall)
        pass

    def throw_barb(self):
        self.switch_animation(HornetAniStatus.Barb_Throw)
        pass

    def sphere_ball(self):
        self.switch_animation(HornetAniStatus.Sphere_Attack)
        pass

    def stop_somebody(self):
        self.switch_animation(HornetAniStatus.Stop_Somebody)
        pass

    pass
