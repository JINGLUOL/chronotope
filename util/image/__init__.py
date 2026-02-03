import numpy as np
from PIL import Image
from PyQt5.QtGui import QImage, QPixmap


def clear_colors_numpy(pixels, *clear_colors):
    """
    使用NumPy快速替换颜色
    :param pixels: 像素数组
    :param clear_colors: 待清除的颜色
    :return:
    """

    # 创建透明遮罩并替换指定颜色
    if len(clear_colors) > 0:
        for clear_color in clear_colors:
            mask = np.all(pixels[:, :, :3] == clear_color[:3], axis=2)
            pixels[mask, 3] = 0
            pass
        pass

    # 转换回PIL图像
    result_image = Image.fromarray(pixels, 'RGBA')

    # 平滑处理
    # result_image = result_image.filter(ImageFilter.SMOOTH)

    return result_image


def replace_color_numpy(pixels, old_color=None, new_color=None):
    """
    使用NumPy快速替换颜色
    :param pixels: 像素数组
    :param old_color: 待替换的颜色
    :param new_color: 替换后的颜色
    :return:
    """

    # 创建遮罩并替换颜色
    if old_color and new_color:
        # 遍历每个像素
        mask = np.all(pixels[:, :, :3] == old_color[:3], axis=2)
        pixels[mask] = new_color[:3]
        pass

    pass


def paste_center_fast(bg: Image, overlay: Image):
    """
    最高效的居中绘制方法
    background: 背景图像
    overlay: 要居中的图像
    """
    # 直接计算居中位置
    x = (bg.width - overlay.width) // 2
    y = (bg.height - overlay.height) // 2

    # 直接粘贴（自动处理透明度）
    bg.paste(overlay, (x, y), overlay)
    return bg


def find_rgb_box_pil(pixels):
    """
    使用PIL检测三原色方框

    参数:
        image_path: 图片路径
        threshold: 颜色通道阈值（0-255）

    返回:
        (x1, y1, x2, y2): 左上角和右下角坐标
    """
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
    x_coords = red_coords[:, 1]
    y_coords = red_coords[:, 0]

    top_left = (np.min(x_coords), np.min(y_coords))
    bottom_right = (np.max(x_coords), np.max(y_coords))

    return top_left, bottom_right


def pil_to_pixmap(pil_image):
    """将PIL Image转换为QPixmap"""
    # 将PIL Image转换为RGB模式（如果不是的话）
    if pil_image.mode == "RGB":
        rgb_image = pil_image
    elif pil_image.mode == "RGBA":
        rgb_image = pil_image
    elif pil_image.mode == "L":  # 灰度图
        rgb_image = pil_image.convert("RGBA")
    else:
        rgb_image = pil_image.convert("RGB")

    # 获取图像数据
    data = rgb_image.tobytes("raw", "RGBA" if rgb_image.mode == "RGBA" else "RGB")

    # 创建QImage
    if rgb_image.mode == "RGBA":
        q_image = QImage(data, rgb_image.width, rgb_image.height, QImage.Format_RGBA8888)
    else:
        q_image = QImage(data, rgb_image.width, rgb_image.height,
                       rgb_image.width * 3, QImage.Format_RGB888)

    # 转换为QPixmap
    pixmap = QPixmap.fromImage(q_image)
    return pixmap
