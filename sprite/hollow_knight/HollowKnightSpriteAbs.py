import abc
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import pygame
from pygame.sprite import Sprite

from global_manager import log
from pygame_component import ContextMenu
from pygame_manager import screen, left_mouse_up_handles, right_mouse_up_handles, finally_handles, framerate
from .HollowKnightAnimation import HollowKnightAnimation, UNDEFINED, create_ani_machine


@dataclass
class SpriteStatus:
    FOLLOW = 'follow'
    CALL = 'call'
    pass


class HollowKnightSpriteAbs(Sprite, abc.ABC):

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
        self.transition_ani: HollowKnightAnimation | None = None
        """ 过渡动画类 """
        self.pre_trans_ani: str = UNDEFINED
        """ 上一个过渡动画 """
        self.sprite_state: str = SpriteStatus.FOLLOW
        """ 精灵状态 """

        # 精灵跟随参数
        self.follow_pass_range: int = 373
        """ 跟随无效范围 """
        self.follow_space_range: int = 99
        """ 跟随距离范围 """

        # 绘制参数
        self.image = self.animation.frames[0]
        """ 超类绘制图 """
        self.x = screen.get_width() - self.image.get_width() - self.animation.current_rect.x - 30
        """ X 轴值 """
        self.y = screen.get_height() - self.image.get_height() - self.animation.current_rect.y - 50
        """ Y 轴值 """
        self.flip_x = False
        """ 左右翻转 """
        self.flip_y = False
        """ 上下翻转 """
        self.rect = pygame.rect.Rect(0, 0, 0, 0)
        """ 更新位置 """
        self.delay: float = framerate*1.35
        # self.delay: int = 300
        """ 更新时间间隔 """
        self.last_update: int = pygame.time.get_ticks()
        """ 最后更新时间 """

        # 额外绘制参数
        self.flip_x_changed: bool = False
        self.flip_y_changed: bool = False
        """ 绘制参数变更 """

        # 初始化菜单
        self.menu = ContextMenu()
        """ 精灵右键菜单 """
        self._setup_menu()

        self.sprite_behavior_map = {
            SpriteStatus.FOLLOW: self._sprite_follow_handle,
            SpriteStatus.CALL: self._sprite_call_handle,
        }
        finally_handles.append(self._sprite_behavior_handle)

        log(self.sprite_name, self.animation_machine.keys())
        pass

    def _sprite_behavior_handle(self):
        self.sprite_behavior_map[self.sprite_state]()
        pass

    @abstractmethod
    def _sprite_follow_handle(self):
        pass

    @abstractmethod
    def _sprite_call_handle(self):
        pass

    def _setup_menu(self):
        """ 设置菜单项 """

        def def1():
            self.sprite_state = SpriteStatus.FOLLOW
            log('switch sprite state:', self.sprite_state)
            pass

        self.menu.add_item("follow", def1)

        def def2():
            self.sprite_state = SpriteStatus.CALL
            log('switch sprite state:', self.sprite_state)
            pass

        self.menu.add_item("call", def2)

        # 添加点击事件
        left_mouse_up_handles.append(self._left_mouse_up_event)
        right_mouse_up_handles.append(self._right_mouse_up_event)
        pass

    def _left_mouse_up_event(self):
        self.menu.handle_click(pygame.mouse.get_pos())
        pass

    def _right_mouse_up_event(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.animation.current_rect.collidepoint(
            mouse_pos[0] - self.x, mouse_pos[1] - self.y
        ):
            if self.menu.visible:
                self.menu.hide()
            else:
                self.menu.show(mouse_pos)
        pass

    def _reset_flip_args(self):
        self.flip_x_changed = False
        self.flip_y_changed = False
        pass

    def _set_flip_x(self, val):
        if self.flip_x is val: return
        self.flip_x = val
        if self.transition_ani: return
        self.flip_x_changed = True
        pass

    def _set_flip_y(self, val):
        if self.flip_y is val: return
        self.flip_y = val
        self.flip_y_changed = True
        pass

    def _set_transition_anim(self, state: str):
        self.transition_ani = self.animation_machine[state]
        self.transition_ani.reset()
        self._reset_flip_args()
        # log('set transition ani', self.transition_ani.name)
        pass

    def _set_anim(self, state: str):
        self.animation_state = state
        self.animation = self.animation_machine[self.animation_state]
        self.animation.reset()
        self._reset_flip_args()
        # log('set ani', self.animation.name)
        pass

    def update(self, *args: Any, **kwargs: Any):
        # 判断下一帧切入时机
        next_frame: bool = False
        if pygame.time.get_ticks() - self.last_update > self.delay:
            self.last_update = pygame.time.get_ticks()
            next_frame = True
            pass

        self.menu.draw(screen)
        # 切入下一帧
        if next_frame:
            # 过渡动画
            if self.transition_ani:
                self.image = self.transition_ani.get_frame()
                # 当动画到最后一帧结束过渡动画
                if self.transition_ani.current_frame == self.transition_ani.sprites:
                    self.transition_ani = None
                    pass
                pass
            # 主动画
            else:
                self.image = self.animation.get_frame()
                pass
            # 根据当前动画参数对帧进行修正
            self.image = pygame.transform.flip(self.image, self.flip_x, self.flip_y)
            pass

        # 更新绘制的位置 | 范围
        self.rect.update(
            self.x, self.y,
            self.image.get_width(), self.image.get_height()
        )
        pass

    @abstractmethod
    def switch_animation(self, state: str):
        """ 切换动画 """
        pass

    pass
