__all__ = ['copy_materials_list', 'print_materials', 'name_id4_to_card_id']

import os

import filetype
import pandas
import pyperclip
from PIL import Image
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox

from libs.c_pyqt5.tool import ImageDialog, InputAreaDialog
from libs.c_pyqt5.window import TransparentWindow
from util.file import copy_a_folders_filename, files_name_only_matching
from util.printer import print_pdf, print_image
from .ImageMergeDialog import ImageMergeDialog

base_folder = r'D:\SharedFolder\国开\报名材料'


def copy_materials_list():
    pyperclip.copy(copy_a_folders_filename(
        base_folder + r'\材料'
    ))
    pass


def print_work(file_path, only_first=True):
    if file_path is None: return
    if not isinstance(file_path, str):
        if isinstance(file_path, QImage):
            print_image(file_path)
            pass
        return
    if filetype.guess(file_path).mime == 'application/pdf':
        if only_first:
            print_pdf(file_path, '1')
        else:
            print_pdf(file_path)
    else:
        print_image(file_path)
    pass


def name_id4_to_card_id(parent: TransparentWindow):
    target_names = InputAreaDialog('输入姓名+身份证后四位的字符串列表', parent).get_input()
    if not target_names: return
    target_names = target_names.split('\n')
    result = []

    data = pandas.read_excel(base_folder + r'\总表.xlsx')
    cols = data.columns.values.tolist()
    names_coli = cols.index('姓名')
    card_ids_coli = cols.index('证件号码')
    for val in data.values:
        name, card_id = val[names_coli], val[card_ids_coli]
        require_name = f"{name}{card_id[-4:]}"
        if require_name in target_names:
            result.append(card_id)
            pass
        pass

    result = '\n'.join(result)
    pyperclip.copy(result)
    return result


def print_materials(parent: TransparentWindow):
    parent.hide()
    printable = QMessageBox.question(
        parent,  # 父窗口
        "确认操作",  # 对话框标题
        "你确定要执行这个操作吗？",  # 询问内容
        QMessageBox.Yes | QMessageBox.No,  # 显示"是"和"否"按钮
        QMessageBox.No  # 默认选中"否"
    ) == QMessageBox.Yes
    """ 是否打印 """
    check_r_c = QMessageBox.question(
        parent,  # 父窗口
        "确认操作",  # 对话框标题
        "是否检查居住证明材料？",  # 询问内容
        QMessageBox.Yes | QMessageBox.No,  # 显示"是"和"否"按钮
        QMessageBox.No  # 默认选中"否"
    ) == QMessageBox.Yes
    """ 是否检查居住证明材料 """

    excel_path = f'{base_folder}\\总表.xlsx'
    data = pandas.read_excel(excel_path)
    cols = data.columns.values.tolist()
    names_coli = cols.index('姓名')
    status_coli = cols.index('问题')
    card_ids_coli = cols.index('证件号码')
    majors_coli = cols.index('专业名称')
    p_level_coli = cols.index('专业层次')

    result = []
    row_index = -1
    for val in data.values:
        row_index += 1
        name, card_id, status, p_level, major = (
            str(val[names_coli]).strip(), str(val[card_ids_coli]).strip(),
            str(val[status_coli]).strip(),
            str(val[p_level_coli]).strip(), str(val[majors_coli]).strip()
        )
        name_aid = f"{name}{card_id[-4:]}"
        if status != '齐' or '护理' in major: continue

        # 登记表位置
        pdf_name = f"{name_aid}.pdf"
        pdf_path = f'{base_folder}\\登记表\\{pdf_name}'
        # 材料位置
        folder_path = f'{base_folder}\\材料\\{name} {card_id}'
        # 判断报名材料是否存在
        pdf_path_une = not os.path.exists(pdf_path)
        folder_path_une = not os.path.exists(folder_path)
        if pdf_path_une or folder_path_une:
            result.append(
                f"{name}{pdf_path_une and '-pdf' or ''}{folder_path_une and '-material' or ''}"
            )
            continue

        # 检查文件完整性
        id_card_front, graduation_certificate, diploma, \
            r_c, r_c1, \
            photo = files_name_only_matching(
            folder_path,
            [
                '身份证正面', '前置学历证书', '前置学历证明材料',
                '其他证明材料', '异地生源证明材料',
                '和招生老师合影',
            ]
        )
        if not r_c: r_c = r_c1

        r_c_result = True
        if r_c and check_r_c:
            r_c_result = ImageDialog('是否通过？', QImage(r_c), parent).get_result()
            pass

        """ ------------------------ """
        # # 1. 加载图片
        # image = QImage(4961, 7016, QImage.Format_RGB32)
        # image.fill(QColor(255, 255, 255))  # 填充白色
        #
        # # 2. 创建 QPainter 对象
        # painter = QPainter(image)
        #
        # # 3. 设置文字样式
        # painter.setPen(QColor(0, 0, 0))  # 设置文字颜色为黑色
        # painter.setFont(QFont("Arial", 29))  # 设置字体和字号
        #
        # # 4. 绘制文字
        # painter.drawText(QPoint(77, 77), name_aid)
        #
        # # 5. 结束绘制
        # painter.end()
        #
        # print_image(photo, duplex_img=image)
        # data.iloc[row_index, status_coli] = 'printed'
        """ ------------------------ """

        # 打印判断
        if printable and r_c_result:
            id_card_img = Image.open(id_card_front)
            diploma_img = Image.open(graduation_certificate and graduation_certificate or diploma)
            merged_img = ImageMergeDialog(
                '生成图片...',
                id_card_img, diploma_img,
                parent
            ).get_result()
            if not merged_img: break

            print_work(pdf_path)
            print_work(merged_img)
            # 判断是否为本科
            if '本科' in p_level:
                print_work(diploma)
            print_work(r_c, False)
            print_work(photo)

            data.iloc[row_index, status_coli] = 'printed'
            pass

        if not r_c_result:
            data.iloc[row_index, status_coli] = 'r_c'
            pass
        pyperclip.copy(card_id)
        pass
    data.to_excel(excel_path, index=False)
    pass


menu_config = {
    '复制报名材料列表': copy_materials_list,
    '姓名加证件号后四位转证件号': name_id4_to_card_id,
    '打印材料': print_materials,
}
