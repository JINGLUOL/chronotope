from collections.abc import Callable
from concurrent.futures.thread import ThreadPoolExecutor

import pygame

from global_manager import config

exit_handles: list[Callable[[], None]] = []

finally_handles: list[Callable[[], None]] = []

left_mouse_down_handles: list[Callable[[], None]] = []
left_mouse_up_handles: list[Callable[[], None]] = []

right_mouse_down_handles: list[Callable[[], None]] = []
right_mouse_up_handles: list[Callable[[], None]] = []

key_down_handles: list[Callable[[], None]] = []
key_up_handles: list[Callable[[], None]] = []

pygame.init()
# 创建视窗，默认隐藏
screen = pygame.display.set_mode(
    (config.screen_root.width, config.screen_root.height),
    flags=pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HIDDEN,
)
framerate: int = 60

def active_handles():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                for handel in left_mouse_down_handles:
                    executor.submit(handel)

            elif event.type == pygame.KEYDOWN:
                for handel in key_down_handles:
                    executor.submit(handel)

            elif event.type == pygame.KEYUP:
                for handel in key_up_handles:
                    executor.submit(handel)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for handel in left_mouse_down_handles:
                        executor.submit(handel)
                elif event.button == 3:
                    for handel in right_mouse_down_handles:
                        executor.submit(handel)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for handel in left_mouse_up_handles:
                        executor.submit(handel)
                elif event.button == 3:
                    for handel in right_mouse_up_handles:
                        executor.submit(handel)

            elif event.type == pygame.MOUSEMOTION:
                # event.rel 是相对移动距离
                # event.buttons 是按下状态的按钮元组
                pass

            pass
        for handel in finally_handles:
            executor.submit(handel)
        pass
    pass
