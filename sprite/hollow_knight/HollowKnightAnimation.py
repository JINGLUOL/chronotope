import os
from concurrent.futures.thread import ThreadPoolExecutor
from typing import AnyStr

import numpy as np
from PIL import Image
from PyQt5.QtGui import QPixmap

from util import str_to_bool
from util.file.image import find_rgb_box_pil, clear_colors_numpy, pil_to_qt_img
from util.geometry import Rect


class HollowKnightAnimBase:

    def __init__(self):
        """ 动画帧初始化 """
        """ 动画参数 """
        self.version: str = '未知'
        self.type: str = '未知'
        self.name: str = '未知'
        self.consistent_sprite_size: bool = True
        self.enable_borders: bool = True
        self.use_sprite_name: bool = False
        self.sprites: int = 0
        ''' 总帧数 '''

        """ 帧参数 """
        self.frames: list[QPixmap] = []
        ''' 帧列表 '''
        self.loop_frame = 0
        ''' 循环起始帧 '''
        self.fps: float = 12
        """ 每秒帧数 """

        """ 角色位置判定范围 """
        self.rects: list[Rect] = []
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
                self.rects.append(Rect.from_pos_and_size(tl, (br[0] - tl[0], br[1] - tl[1])))
                # 添加到帧序列
                self.frames.append(QPixmap.fromImage(pil_to_qt_img(image)))
                del pixels
                pass
            pass
        self.consistent_sprite_size = str_to_bool(self.consistent_sprite_size)
        self.enable_borders = str_to_bool(self.enable_borders)
        self.use_sprite_name = str_to_bool(self.use_sprite_name)
        self.sprites = int(self.sprites)
        
        self.fps = int(self.fps)
        self.loop_frame = int(self.loop_frame)
        pass

    pass


class HollowKnightAnimation:

    def __init__(self, hollow_knight_base: HollowKnightAnimBase):
        """ 初始化动画类 """
        """ 动画参数 """
        self.version: str = hollow_knight_base.version
        self.type: str = hollow_knight_base.type
        self.name: str = hollow_knight_base.name
        self.consistent_sprite_size: bool = hollow_knight_base.consistent_sprite_size
        self.enable_borders: bool = hollow_knight_base.enable_borders
        self.use_sprite_name: bool = hollow_knight_base.use_sprite_name
        self.sprites: int = hollow_knight_base.sprites
        ''' 总帧数 '''
        self.loop_frame = hollow_knight_base.loop_frame
        ''' 循环起始帧 '''

        self.frames: list[QPixmap] = hollow_knight_base.frames
        ''' 帧列表 '''
        self.rects: list[Rect] = hollow_knight_base.rects
        """ 角色碰撞判定集 """

        self.delay: float = 1000 / hollow_knight_base.fps

        self.start_frame: int = 0
        ''' 设置起始帧 '''
        self.current_frame = 0
        ''' 当前帧 '''
        self.in_loop: bool = False
        ''' 进入循环帧 '''
        self.current_rect = self.rects[self.current_frame]
        ''' 角色碰撞矩形 '''
        pass

    def reset(self):
        self.start_frame = 0
        self.current_frame = 0
        self.current_rect = self.rects[self.current_frame]
        self.in_loop = False
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

    pass


loaded_anim_base_map: dict[str, dict[str, HollowKnightAnimBase]] = {}
""" 空洞骑士资源加载缓存表 """


def create_ani_machine(ani_root: str) -> dict[str, HollowKnightAnimation]:
    """ 创建动画机 """
    # 资源缓存字典存在时直接返回，避免重复读取资源
    global loaded_anim_base_map
    if ani_root not in loaded_anim_base_map:
        # 动画机对象
        animation_base = {}
        # 添加动画机对象到字典，避免重复读取资源
        loaded_anim_base_map[ani_root] = animation_base

        # 资源配置根目录
        configs_root = f"{ani_root}\\config"

        # 初始化动画源
        def work(config_file):
            """ 根据 资源配置文件 进行初始化状态 """
            with open(f"{configs_root}\\{config_file}", 'r', encoding='utf-8') as f:
                animation = HollowKnightAnimBase()
                animation.load_animation(ani_root, f.readlines())
                animation_base[animation.name] = animation
                pass
            pass

        """ 调用线程池初始化，避免加载时间冗长 """
        with ThreadPoolExecutor(max_workers=9) as executor:
            for ani_config in os.listdir(configs_root):
                executor.submit(work, ani_config)
                pass
            pass
        pass
    # 初始化动画机器
    animation_machine: dict[str, HollowKnightAnimation] = {}
    for sprite in loaded_anim_base_map[ani_root]:
        animation_machine[sprite] = HollowKnightAnimation(loaded_anim_base_map[ani_root][sprite])
        pass
    return animation_machine
