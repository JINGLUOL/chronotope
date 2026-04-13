import subprocess
from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QImage, QTransform
from PyQt5.QtPrintSupport import QPrinter

from global_manager import resources


@dataclass
class PrinterSettings:
    SIMPLEX: str = 'simplex'
    ''' 单面打印 '''
    DUPLEX: str = "duplex"
    ''' 长边翻转 '''
    DUPLEX_SHORT: str = "duplexshort"
    ''' 短边翻转 '''

    FIT: str = "fit"
    ''' 强制缩放内容以完全匹配打印纸张 '''
    SHRINK: str = "shrink"
    ''' 仅当内容过大时缩小以适合纸张，内容过小时保持原大小 '''
    NO_SCALE: str = "noscale"
    ''' 完全不缩放，按原始尺寸打印，超出纸张部分会被裁切 '''

    IMG_FIT_NORMAL = 'normal'
    ''' 按设置的位置/大小打印 '''

    A3: str = "A3"
    A4: str = "A4"
    pass


def print_image(
        image: str | QImage, fit=PrinterSettings.FIT,
        duplex_img: str | QImage = None, duplex_mod=QPrinter.DuplexMode.DuplexShortSide,
):
    """
    精确打印图片，可控制位置和大小
    :param image: 图片文件路径
    :param fit: 图片适应模式
    :param duplex_img: 背面图片
    :param duplex_mod: 双面打印模式
    """"""核心打印函数"""

    # 创建打印机对象
    printer = QPrinter()
    if duplex_img is not None:
        printer.setDuplex(duplex_mod)
        pass

    # 创建QPainter，并指定绘制设备为刚刚配置好的printer
    painter = QPainter(printer)

    # 获取纸张的可打印区域（视口）矩形
    viewport_rect = painter.viewport()

    print_index = 0
    for img in (image, duplex_img):
        if img is None: break
        if print_index > 0: printer.newPage()

        # 获取图片对象
        if isinstance(img, str):
            img = QImage(img)
            pass

        # 获取图片的原始尺寸
        image_size = img.size()

        # 图片自适应
        if fit == PrinterSettings.FIT and image_size.width() > image_size.height():
            img = img.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
            image_size = img.size()
            pass

        # 缩放图片尺寸，使其适应纸张，同时保持宽高比
        image_size.scale(viewport_rect.size(), Qt.KeepAspectRatio)

        # 重新设置QPainter的视口，使图片居中或位于指定位置
        painter.setViewport(viewport_rect.x(), viewport_rect.y(),
                            image_size.width(), image_size.height())

        # 设置QPainter的窗口为图片的完整矩形，确保后续绘制使用图片的坐标系
        painter.setWindow(img.rect())

        # 在(0,0)点绘制图片，由于上面已经做了坐标映射，图片会自动绘制到纸张中心
        painter.drawImage(0, 0, img)
        print_index += 1
        pass

    # 结束绘制，这对于打印机来说至关重要，它会触发实际的打印动作
    painter.end()
    print(f"图片已发送到打印机")
    pass


def print_pdf(
        pdf_path,
        page_range='all',
        fit=PrinterSettings.SHRINK,
        duplex=PrinterSettings.SIMPLEX,
        paper=PrinterSettings.A4
):
    cmd = [
        resources.SumatraPDF,
        "-print-to-default",
        "-print-settings",
        f"{page_range},fit={fit},{duplex},paper={paper}",
        "-silent",
        pdf_path,
    ]

    subprocess.run(cmd, check=True)
    print(f"PDF已发送到打印机")
    pass
