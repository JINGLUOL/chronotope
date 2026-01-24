import numpy as np
import pygame
from pygame import Surface


def replace_color_numpy(
        surface: Surface,
        *clear_colors,
        old_color = None, new_color = None,
):
    """
    使用NumPy快速替换颜色
    :param surface: pygame的绘制对象
    :param clear_colors: 待清除的颜色
    :param old_color: 待替换的颜色
    :param new_color: 替换后的颜色
    :return:
    """
    # 将surface转换为NumPy数组
    pixels = pygame.surfarray.pixels3d(surface)

    # 创建遮罩并替换颜色
    if old_color and new_color:
        # 遍历每个像素
        mask = np.all(pixels == old_color[:3], axis=2)
        pixels[mask] = new_color[:3]
        pass

    # 创建透明遮罩并替换指定颜色
    if len(clear_colors) > 0:
        pixels_alpha = pygame.surfarray.pixels_alpha(surface)
        for clear_color in clear_colors:
            mask = np.all(pixels == clear_color[:3], axis=2)
            pixels_alpha[mask] = 0
            pass
        pass


    # 注意：surfarray.pixels3d会自动锁定surface
    # 操作完成后，删除对pixels的引用以解锁
    del pixels
    pass


def find_rgb_box_pil(surface: Surface):
    """
    使用PIL检测三原色方框

    参数:
        image_path: 图片路径
        threshold: 颜色通道阈值（0-255）

    返回:
        (x1, y1, x2, y2): 左上角和右下角坐标
    """
    pixels = pygame.surfarray.pixels3d(surface)
    # 分离RGB通道
    red_channel = pixels[:, :, 0]
    green_channel = pixels[:, :, 1]
    blue_channel = pixels[:, :, 2]

    # 创建颜色掩膜（例：红色值高，绿色和蓝色值低）
    threshold = 200
    mask = (red_channel > threshold) & (green_channel < threshold / 2) & (blue_channel < threshold / 2)

    # 找到红色像素的坐标
    red_coords = np.column_stack(np.where(mask))

    if len(red_coords) == 0:
        print("未找到红色像素")
        return (0, 0), (0, 0)

    # 计算边界
    x_coords = red_coords[:, 0]
    y_coords = red_coords[:, 1]

    top_left = (np.min(x_coords), np.min(y_coords))
    bottom_right = (np.max(x_coords), np.max(y_coords))

    del pixels
    return top_left, bottom_right
