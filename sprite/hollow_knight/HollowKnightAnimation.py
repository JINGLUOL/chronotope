import os
from concurrent.futures.thread import ThreadPoolExecutor
from typing import AnyStr

import numpy as np
from PIL import Image
from PyQt5.QtGui import QPixmap

from util import str_to_bool
from util.geometry import Rect
from util.image import find_rgb_box_pil, clear_colors_numpy, pil_to_pixmap

UNDEFINED: str = 'UNDEFINED'


class HollowKnightAnimation:

    def __init__(self):
        """ 动画帧初始化 """
        """ 动画参数 """
        self.version: str = UNDEFINED
        self.type: str = UNDEFINED
        self.name: str = UNDEFINED
        self.consistent_sprite_size: bool = True
        self.enable_borders: bool = True
        self.use_sprite_name: bool = False
        self.sprites: int = 0
        ''' 总帧数 '''

        """ 帧参数 """
        self.frames: list[QPixmap] = []
        ''' 帧列表 '''
        self.current_frame = 0
        ''' 当前帧 '''
        self.loop_frame = 0
        ''' 循环起始帧 '''
        self.in_loop: bool = False
        ''' 进入循环帧 '''
        self.start_frame: int = 0
        ''' 设置起始帧 '''

        """ 角色位置判定范围 """
        self.rects: list[Rect] = []
        self.current_rect: Rect = Rect((0, 0), (0, 0))
        pass

    def get_frame(self) -> QPixmap:
        """ 获取帧 """
        self.current_frame %= self.sprites

        # 设置并锁定到循环帧
        self.current_frame = max(self.current_frame, self.start_frame)
        if not self.in_loop and self.current_frame >= self.loop_frame:
            self.in_loop = True
            self.start_frame = self.loop_frame
            pass

        frame = self.frames[self.current_frame]
        self.current_rect = self.rects[self.current_frame]

        # 切换下一帧
        self.current_frame += 1
        return frame

    def reset(self):
        self.start_frame = 0
        self.current_frame = 0
        self.current_rect = self.rects[self.current_frame]
        self.in_loop = False
        pass

    def load_animation(self, ani_root: str, config_lines: list[AnyStr]):
        kv_split_str = ': '
        frames_split_str = '	'
        for line in config_lines:
            line = line.strip()
            if kv_split_str in line:
                key, value = line.split(kv_split_str)
                setattr(self, key, value)
                pass
            elif frames_split_str in line:
                image = Image.open(
                    f"{ani_root}\\{line.split(frames_split_str)[1]}"
                ).convert('RGBA')
                pixels = np.array(image)
                # 处理红框
                image = clear_colors_numpy(pixels, (255, 0, 0))
                # 检索角色在图片上的范围坐标
                tl, br = find_rgb_box_pil(pixels)
                self.rects.append(Rect(tl, (br[0] - tl[0], br[1] - tl[1])))
                # 添加到帧序列
                self.frames.append(pil_to_pixmap(image))
                del pixels
                pass
            pass
        self.consistent_sprite_size = str_to_bool(self.consistent_sprite_size)
        self.enable_borders = str_to_bool(self.enable_borders)
        self.use_sprite_name = str_to_bool(self.use_sprite_name)
        self.sprites = int(self.sprites)
        self.loop_frame = int(self.loop_frame)

        self.current_rect = self.rects[self.current_frame]
        pass

    pass


def create_ani_machine(ani_root: str) -> dict[str, HollowKnightAnimation]:
    """ 创建动画机 """
    animation_machine = {}
    configs_root = f"{ani_root}\\config"

    def work(config_file):
        with open(f"{configs_root}\\{config_file}", 'r', encoding='utf-8') as f:
            animation = HollowKnightAnimation()
            animation.load_animation(ani_root, f.readlines())
            animation_machine[animation.name] = animation
            pass
        pass

    """ 初始化动画机器 """
    with ThreadPoolExecutor(max_workers=9) as executor:
        for ani_config in os.listdir(configs_root):
            executor.submit(work, ani_config)
            pass
        pass
    return animation_machine
