from abc import abstractmethod

from global_manager import log
from global_manager import screen
from .HollowKnightAnimation import HollowKnightAnimation, UNDEFINED, create_ani_machine
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
        self.transition_ani: HollowKnightAnimation | None = None
        """ 过渡动画类 """
        self.pre_trans_ani: str = UNDEFINED
        """ 上一个过渡动画 """
        self.delay: float = 81
        # self.delay: int = 300
        """ 更新时间间隔 """
        self.last_update: float = 0
        """ 最后更新时间 """

        # 精灵跟随参数
        self.follow_pass_range: int = 373
        """ 跟随无效范围 """
        self.follow_space_range: int = 99
        """ 跟随距离范围 """

        # 绘制参数
        self.image = self.animation.frames[0]
        """ 绘制图 """
        self.sprite_x = screen.get_width() - self.image.width() - self.animation.current_rect.x - 30
        """ X 轴值 """
        self.sprite_y = screen.get_height() - self.image.height() - self.animation.current_rect.y - 50
        """ Y 轴值 """
        self.flip_x = False
        """ 左右翻转 """
        self.flip_y = False
        """ 上下翻转 """

        # 额外绘制参数
        self.flip_x_changed: bool = False
        self.flip_y_changed: bool = False
        """ 绘制参数变更 """

        # 初始化图片
        self.setPixmap(self.image)

        # 输出精灵的所有状态
        log(self.sprite_name, self.animation_machine.keys())
        pass

    @abstractmethod
    def _sprite_follow_handle(self):
        pass

    @abstractmethod
    def _sprite_call_handle(self):
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

    def update_anim(self, current_time: float):
        # 切入下一帧
        if current_time - self.last_update > self.delay:
            self.last_update = current_time
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
            # 切换帧图
            self.setPixmap(self.image)
            pass

        # 更新绘制的位置
        self.setPos(self.sprite_x, self.sprite_y)
        pass

    @abstractmethod
    def switch_animation(self, state: str):
        """ 切换动画 """
        pass

    pass
