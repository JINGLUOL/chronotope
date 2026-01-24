import sys

from pygame_manager import screen, active_handles, exit_handles, framerate
import pygame

from Window import Window
from cos.win import to_util_window, bring_to_front
from factory import *
from global_manager import config


class PyGameWindow(Window):

    def __init__(self, width, height):
        super().__init__(width, height)

        # 透明色
        self.transparent_color = pygame.Color(config.TRANSPARENT_COLOR)

        # Windows获取窗口句柄
        self.hwnd = pygame.display.get_wm_info()["window"]

        # 设置为透明工具窗口
        to_util_window(self.hwnd, config.TRANSPARENT_COLOR_VAL)

        # 帧数锁
        self.clock = pygame.time.Clock()

        # 精灵工厂
        self.sprite_factory = SpriteFactory()

        # 显示窗口
        self.get_focus()

        # 添加事件
        exit_handles.append(self.quit_app)
        pass

    def get_focus(self):
        bring_to_front(self.hwnd)
        pass

    def run(self):
        clock = self.clock
        while self.running:
            # 事件处理
            active_handles()

            # 清屏
            screen.fill(self.transparent_color)

            # 绘制
            if not self.hidden:
                self.sprite_factory.sprites_update()
                pass

            # 更新显示
            pygame.display.flip()

            # 控制帧率
            clock.tick(framerate)
            pass
        self.key_listener.stop()
        pygame.quit()
        sys.exit()

    pass
