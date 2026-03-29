__all__ = ['copy_materials_list', 'print_materials', 'name_id4_to_card_id']

import os

import filetype
import pandas
import pyperclip
from PIL import Image
from PyQt5.QtGui import QImage

from pyqt.qt5.util.InputAreaDialog import InputAreaDialog
from pyqt.qt5.window import TransparentWindow
from util.file import copy_a_folders_filename, files_name_only_matching
from util.printer import print_pdf, print_image
from .ImageDialog import ImageDialog

base_folder = r'D:\SharedFolder\国开\报名材料'


def copy_materials_list():
    pyperclip.copy(copy_a_folders_filename(
        base_folder + r'\材料',
        '[0-9a-zA-Z]+'
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


def name_id4_to_card_id():
    target_names = InputAreaDialog('输入姓名+身份证后四位的字符串列表').get_input()
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


def create_id_card_and_diploma_img():
    return


def print_materials(parent: TransparentWindow):
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
            str(val[names_coli]), str(val[card_ids_coli]),
            str(val[status_coli]),
            str(val[p_level_coli]), str(val[majors_coli])
        )
        if 'printed' in status or '打印' in status or '护理' in major: continue

        # 登记表位置
        pdf_name = f"{name}{card_id[-4:]}.pdf"
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
        id_card_front, \
            graduation_certificate, \
            diploma, \
            r_c, \
            photo = \
            files_name_only_matching(
                folder_path,
                ['身份证正面', '前置学历证书', '前置学历证明材料', '其他证明材料', '和招生老师合影']
            )

        id_card_img = Image.open(id_card_front)
        diploma_img = Image.open(graduation_certificate and graduation_certificate or diploma)
        merged_img = ImageDialog(
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
        pyperclip.copy(card_id)
        pass
    data.to_excel(excel_path, index=False)
    pass
