from abc import abstractmethod

from PyQt5.QtGui import QPixmap

from global_manager import log
from global_manager import screen
from .HollowKnightAnimation import HollowKnightAnimation, create_ani_machine
from ..SpriteAbs import SpriteAbs


class HollowKnightSpriteAbs(SpriteAbs):

    def __init__(
            self,
            sprite_name: str, setup_ani_state: str,
            resources_root: str
    ):
        super().__init__()

        self.sprite_name = sprite_name
        """ 精灵名称 """

        # 初始化状态机器
        self.animation_machine: dict[str, HollowKnightAnimation] = create_ani_machine(resources_root)
        """ 动画机器 """

        # 动画参数
        self.animation_state: str = setup_ani_state
        """ 动画状态 """
        self.animation: HollowKnightAnimation = self.animation_machine[self.animation_state]
        """ 动画类 """
        self.effect_anim_list: list[HollowKnightAnimation] = []
        """ 效果动画类序列 """
        self.effect_anim_set: set[str] = set()
        """ 效果动画类集合 """
        self.transition_anim_list: list[HollowKnightAnimation] = []
        """ 过渡动画类序列 """
        self.transition_anim_set: set[str] = set()
        """ 过渡动画类集合 """
        self.last_update: float = 0
        """ 最后更新时间 """
        self.effect_last_update: float = 0
        """ 特效最后更新时间 """
        self.effect_loop: bool = False
        """ 特效循环 """
        self.anim_delay: float = self.animation.delay
        self.transition_delay: float = self.animation.delay
        self.effect_delay: float = self.animation.delay

        # 绘制参数
        self.image: QPixmap = self.animation.frames[0]
        """ 源动画图 """
        self.transition_image: QPixmap = self.animation.frames[0]
        """ 过渡动画图 """
        self.effect_image: QPixmap = self.animation.frames[0]
        """ 效果动画图 """
        self.sprite_x = screen.get_width() - self.image.width()
        """ X 轴值 """
        self.sprite_y = screen.get_height() - self.image.height()
        """ Y 轴值 """
        self.flip_x = False
        """ 左右翻转 """
        self.flip_y = False
        """ 上下翻转 """

        # 精灵跟随参数
        self.follow_space_range: int = 233
        """ 跟随距离范围 """
        self.follow_pass_range: int = 466
        """ 跟随无效范围 """

        # 额外绘制参数
        self.flip_x_changed: bool = False
        self.flip_y_changed: bool = False
        """ 绘制参数变更 """

        # 初始化图片和位置
        self.setPixmap(self.image)
        self.setPos(self.sprite_x, self.sprite_y)

        # 输出精灵的所有状态
        log(self.sprite_name, self.animation_machine.keys())
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

    def _set_flip_x(self, val):
        if self.flip_x is val: return
        self.flip_x = val
        if self.is_transitioning(): return
        self.flip_x_changed = True
        pass

    def _set_flip_y(self, val):
        if self.flip_y is val: return
        self.flip_y = val
        self.flip_y_changed = True
        pass

    def _reset_flip_args(self):
        self.flip_x_changed = False
        self.flip_y_changed = False
        pass

    def _set_anim(self, state: str):
        self.animation_state = state
        self.animation = self.animation_machine[self.animation_state]
        self.animation.reset()
        self.anim_delay = self.animation.delay
        self._reset_flip_args()
        # log('set ani', state)
        pass

    def _set_transition_anim(self, state: str):
        anim = self.animation_machine[state]
        anim.reset()
        self._reset_flip_args()
        self.transition_anim_list.append(anim)
        self.transition_anim_set.add(state)
        self.transition_delay = self.transition_anim_list[0].delay
        # log('set transition ani', state)
        pass

    def _set_effect_anim(self, state: str):
        anim = self.animation_machine[state]
        anim.reset()
        self.effect_anim_list.append(anim)
        self.effect_anim_set.add(state)
        self.effect_delay = self.effect_anim_list[0].delay
        pass

    def _set_image(self, image: QPixmap):
        self.image = image
        # 切换帧图
        self.setPixmap(image.transformed(self.transform().scale(
            self.flip_x and -1 or 1,
            self.flip_y and -1 or 1
        )))
        pass

    def _set_transition_image(self, image: QPixmap):
        self.transition_image = image
        self.transition_item.setPixmap(image.transformed(self.transform().scale(
            self.flip_x and -1 or 1,
            self.flip_y and -1 or 1
        )))
        if self.scene():
            offset_x = (self.image.rect().width() - image.rect().width()) / 2
            offset_y = (self.image.rect().height() - image.rect().height()) / 2
            self.hide()
            self.transition_item.setZValue(self.zValue())
            self.transition_item.setPos(self.x() + offset_x, self.y() + offset_y)
            self.transition_item.show()
            pass
        pass

    def _remove_transition_item(self):
        self.transition_item.hide()
        pass

    def _set_effect_image(self, image: QPixmap):
        self.effect_image = image
        self.effect_item.setPixmap(image.transformed(self.transform().scale(
            self.flip_x and -1 or 1,
            self.flip_y and -1 or 1
        )))
        offset_x = (self.image.rect().width() - image.rect().width()) / 2
        offset_y = (self.image.rect().height() - image.rect().height()) / 2
        self.effect_item.setPos(self.x() + offset_x, self.y() + offset_y)
        self.effect_item.setZValue(self.zValue() + 1)
        self.effect_item.show()
        pass

    def _remove_effect_item(self):
        self.effect_item.hide()
        pass

    def is_transitioning(self) -> bool:
        return len(self.transition_anim_list) > 0

    def is_effect_transitioning(self) -> bool:
        return len(self.effect_anim_list) > 0

    def update_anim(self, current_time: float):
        """ 切帧 | 更替动画 """

        # 过渡动画
        if self.is_transitioning():
            if current_time - self.last_update > self.transition_delay:
                self.last_update = current_time
                transition_anim = self.transition_anim_list[0]
                self._set_transition_image(transition_anim.get_frame())
                # 当动画到最后一帧结束过渡动画
                if transition_anim.current_frame >= transition_anim.sprites:
                    self.transition_anim_list.remove(transition_anim)
                    self.transition_anim_set.discard(transition_anim.name)
                    # 切换动画fps
                    if self.is_transitioning():
                        self.transition_delay = self.transition_anim_list[0].delay
                    pass
                pass
        else:
            # 效果动画
            if (
                    self.is_effect_transitioning() and
                    current_time - self.effect_last_update > self.effect_delay
            ):
                self.effect_last_update = current_time
                effect_anim = self.effect_anim_list[0]
                self._set_effect_image(effect_anim.get_frame())
                if not self.effect_loop and effect_anim.current_frame >= effect_anim.sprites:
                    self.effect_anim_list.remove(effect_anim)
                    self.effect_anim_set.discard(effect_anim.name)
                    # 切换动画fps
                    if self.is_effect_transitioning():
                        self.effect_delay = self.effect_anim_list[0].delay
                    else:
                        self._remove_effect_item()
                    pass
                pass
            if current_time - self.last_update > self.anim_delay:
                self.last_update = current_time
                self._set_image(self.animation.get_frame())
                self.show()
                self._remove_transition_item()
            pass

        # 更新绘制的位置
        self.setPos(self.sprite_x, self.sprite_y)
        pass

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)

        self.click_offset_x = self.animation.current_rect.x + self.animation.current_rect.w / 2
        self.click_offset_y = self.animation.current_rect.y + self.animation.current_rect.h / 2
        pass

    @abstractmethod
    def switch_animation(self, state: str):
        """ 切换动画 """
        pass

    pass
