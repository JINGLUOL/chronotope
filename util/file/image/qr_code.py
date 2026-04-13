import os

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def create_qr_code(data, save_path, file_name=None):
    if not os.path.exists(save_path):
        return
    # 使用最简单的make()函数一步生成
    img = qrcode.make(data)

    # 保存为图片文件
    if file_name:
        img.save(f"{save_path}\\{file_name}.png")
    else:
        img.save(f"{save_path}\\qr_code.png")
    pass

# # 创建一个QRCode对象，精细控制每个参数
# qr = qrcode.QRCode(
#     version=1,  # 控制二维码的尺寸，1最小（21x21）
#     error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高纠错率，方便嵌入Logo
#     box_size=10,  # 每个“点”的像素大小
#     border=1,  # 边框宽度
# )
# qr.add_data(data)
# qr.make(fit=True)
#
# # 生成一个带圆角模块的彩色二维码
# img = qr.make_image(
#     image_factory=StyledPilImage,  # 使用样式工厂
#     # module_drawer=RoundedModuleDrawer(),  # 使用圆角绘制器
#     fill_color=(0, 0, 255),  # 前景色（蓝色）
#     back_color=(255, 255, 255)  # 背景色（白色）
# )
# img.save(r"C:\Users\Rvny_\Desktop\test.png")
