import os

from PIL import Image


def center_crop(image_path, crop_width, crop_height, output_path):
    """
    将图片居中裁剪为指定尺寸
    :param image_path: 输入图片路径
    :param crop_width: 目标裁剪宽度
    :param crop_height: 目标裁剪高度
    :param output_path: 输出图片路径
    """
    # 1. 打开图片
    if isinstance(image_path, Image.Image):
        img = image_path
    else:
        img = Image.open(image_path)
    original_width, original_height = img.size

    # 2. 计算裁剪区域的左上角坐标
    left = (original_width - crop_width) // 2
    top = (original_height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height

    # 3. 执行裁剪
    cropped_img = img.crop((left, top, right, bottom))

    # 4. 保存结果
    cropped_img.save(output_path)
    print(f"裁剪完成，已保存至：{output_path}")
    pass


def resize_cover(image_path, target_size, output_path):
    """
    将图片等比例缩放至完全覆盖目标尺寸（覆盖模式），然后居中裁剪
    :param image_path:  输入图片路径
    :param target_size: 目标尺寸 (width, height)
    :param output_path: 输出图片路径
    """
    img = Image.open(image_path)
    original_width, original_height = img.size
    target_width, target_height = target_size

    # 计算缩放比例（取较大的比例，确保覆盖目标矩形）
    ratio = max(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # 等比例缩放
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # 居中裁剪
    center_crop(img_resized, target_width, target_height, output_path)
    print(f"覆盖缩放完成：{output_path}")


if __name__ == '__main__':
    resource_dir = r'C:\Users\Rvny_\Desktop\新建文件夹 (2)'
    target_dir = r'C:\Users\Rvny_\Desktop\新建文件夹'
    for fn in os.listdir(resource_dir):
        print(fn)
        # 使用示例
        resize_cover(
            os.path.join(resource_dir, fn),
            (240, 320),
            os.path.join(target_dir, '-' in fn and fn or fn.replace('_', '-')),
        )
        pass
    pass
