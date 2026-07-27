from collections import deque

from PyQt5.QtCore import Qt, QRegularExpression, pyqtSignal
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QPushButton, QDialog, QCheckBox, \
    QScrollArea, QButtonGroup, QFrame

from .DebouncedLineEdit import DebouncedLineEdit
from .NoWheelComboBox import NoWheelComboBox
from .SettingUnit import SettingUnit, SettingTextUnit, SettingOptionUnit, SettingGroupUnit, SettingTextUnitTypes, \
    SettingOptionUnitTypes
from .SimpleTreeWidget import SimpleTreeWidget
from ...label import ElidedLabel

_LINE_OPTION_NUM: int = 2


class SimpleSettingDialog(QDialog):
    confirm_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent:
            self.setMinimumSize(parent.size() * (2/3))
            pass

        self.setting_abs_path = QLabel(self)
        ''' 树状列表的绝对路径 '''

        self.page_map = SimpleTreeWidget(self)
        ''' 页面列表树状图 '''
        self.page_controller = QStackedWidget()
        ''' 设置页面控制器 '''

        # 声明底部控件
        self.confirm_btn = QPushButton('确认')
        ''' 确认按钮 '''
        self.cancel_btn = QPushButton('取消')
        ''' 取消按钮 '''
        self.apply_btn = QPushButton('应用')
        ''' 应用按钮 '''

        self._init_ui()
        self._mount_event()
        pass

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # 声明整体控件
        header = QWidget(self)
        body = QWidget(self)
        footer = QWidget(self)

        # 填充整体控件
        layout.addWidget(header)
        layout.addWidget(body)
        layout.addWidget(footer)

        # 声明整体布局
        header_layout = QHBoxLayout(header)
        body_layout = QHBoxLayout(body)
        footer_layout = QHBoxLayout(footer)

        # 声明头部控件
        setting_abs_path = self.setting_abs_path
        # 填充头部控件
        header_layout.addWidget(setting_abs_path)

        # 声明主体控件
        page_map = self.page_map
        ''' 页面列表树状图 '''
        page_controller = self.page_controller
        ''' 设置页面控制器 '''
        # 填充主体控件
        body_layout.addWidget(page_map, 1)
        body_layout.addWidget(page_controller, 3)

        # 填充底部控件
        footer_layout.addStretch(3)
        footer_layout.addWidget(self.confirm_btn)
        footer_layout.addWidget(self.cancel_btn)
        footer_layout.addWidget(self.apply_btn)
        pass

    def _mount_event(self):
        self.page_map.item_clicked_signal.connect(self.page_controller.setCurrentIndex)
        self.confirm_btn.clicked.connect(self.confirm_signal.emit)
        self.cancel_btn.clicked.connect(self.reject)
        self.apply_btn.clicked.connect(self.accept)
        pass

    def _load_setting_unit(self, unit: SettingUnit) -> deque[QWidget | list]:
        result = deque()
        # 文本设置控件
        if isinstance(unit, SettingTextUnit):
            # 强调类型
            unit: SettingTextUnit = unit
            # 声明文本设置主体控件
            widget = QWidget()
            layout = QHBoxLayout(widget)
            # 声明提示控件
            attr_label = ElidedLabel(unit.name)
            if unit.description: attr_label.setToolTip(unit.description)
            # 声明编辑控件 | 初始化编辑控件内容
            text_edit = DebouncedLineEdit(unit.get_attr())
            text_edit.stopTyping.connect(
                lambda new_val: unit.set_attr(new_val)
                if text_edit.hasAcceptableInput()
                else None
            )
            # 定义文本限制
            if unit.type is SettingTextUnitTypes.INT:
                text_edit.setPlaceholderText('整数')
                text_edit.setValidator(QIntValidator())
            elif unit.type is SettingTextUnitTypes.FLOAT:
                text_edit.setPlaceholderText('浮点数')
                text_edit.setValidator(QDoubleValidator())
            else:
                text_edit.setPlaceholderText(unit.regex)
                if unit.regex != '.*':
                    text_edit.setValidator(QRegularExpressionValidator(QRegularExpression(
                        unit.regex
                    )))
                    pass
                pass
            # 填充文本设置控件
            layout.addWidget(attr_label, 3)
            layout.addWidget(text_edit, 7)

            # 添加到结果集
            result.append(widget)
        # 选项设置控件
        elif isinstance(unit, SettingOptionUnit):
            # 强调类型
            unit: SettingOptionUnit = unit
            # 声明选项设置主体控件
            widget = QWidget()
            layout = QHBoxLayout(widget)
            # 声明子布局
            body_layout = QVBoxLayout(widget)
            # 声明提示控件
            attr_label = QLabel(unit.name)
            attr_label.setToolTip(unit.description)
            # 判断选择类型
            if unit.type is SettingOptionUnitTypes.COMBO:
                # 声明选项列表控件
                option_widget = NoWheelComboBox()
                # 添加选项列表
                option_widget.addItems(unit.options)
                # 设置默认值
                selected_i = unit.options.index(unit.get_attr())
                option_widget.setCurrentIndex(selected_i if selected_i != -1 else 0)
                # 连接值变化的信号
                option_widget.currentTextChanged.connect(unit.set_attr)
                # 添加至布局
                body_layout.addWidget(option_widget)
                pass
            else:
                l = len(unit.options)
                option_widget = QButtonGroup(widget)
                option_widget.setExclusive(unit.type == SettingOptionUnitTypes.SINGLE)
                for i in range(l)[::_LINE_OPTION_NUM]:
                    o_layout = QHBoxLayout()
                    for j in range(_LINE_OPTION_NUM):
                        index = i + j
                        if index >= l: break
                        text = unit.options[index]
                        o = QCheckBox(text)
                        option_widget.addButton(o, index)
                        if index in unit.selected_indexes: o.setChecked(True)
                        o_layout.addWidget(o)
                        pass
                    body_layout.addLayout(o_layout)
                    pass
                option_widget.buttonClicked.connect(
                    lambda btn: unit.set_attr(btn.text())
                    if btn.isChecked() else unit.del_attr(btn.text())
                )
                pass
            # 填充选项设置控件
            layout.addWidget(attr_label, alignment=Qt.AlignTop | Qt.AlignLeft)
            layout.addLayout(body_layout)

            # 添加到结果集
            result.append(widget)
        # 设置控件组
        elif isinstance(unit, SettingGroupUnit):
            group_widgets: list = [self._load_setting_unit(u) for u in unit.units]
            group_widgets.append(unit)
            result.append(group_widgets)
            pass

        # --- 添加水平分割线 ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # 水平线
        line.setFrameShadow(QFrame.Sunken)  # 可选阴影效果（或 QFrame.Raised）
        result.append(line)

        return result

    def _create_group_widget(self, items: list | deque[list | deque]) -> QWidget:
        part = QWidget()
        part.setProperty('class', 'card')
        layout = QVBoxLayout(part)

        if isinstance(items, list):
            unit: SettingGroupUnit = items.pop()
            title = QLabel(unit.name)
            title.setToolTip(unit.description)
            layout.addWidget(title)
            pass

        for item in items:
            if isinstance(item, list):
                part_widget = QWidget()
                part_layout = QVBoxLayout(part_widget)

                for i in item: part_layout.addWidget(i)
                layout.addWidget(part_widget)
                pass
            elif isinstance(item, deque):
                layout.addWidget(self._create_group_widget(item))
            elif isinstance(item, QWidget):
                layout.addWidget(item)
            pass
        return part

    def _load_setting_pages(
            self,
            units: dict[str, list[SettingUnit] | dict[str, list[SettingUnit]]]
    ):
        """ 加载设置页面 """
        for page_title, units in units.items():
            if isinstance(units, dict):
                self._load_setting_pages(units)
            else:
                scroll = QScrollArea()
                ''' 滚动控件 '''
                # 设置滚动控件行为
                scroll.setWidgetResizable(True)  # 让内容控件可自适应宽度
                # scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 始终显示垂直滚动条

                page = QWidget()
                ''' 页面控件 '''
                layout = QHBoxLayout(page)
                body = QVBoxLayout()
                # 添加主体 | 两边弹性边距
                layout.addStretch(1)
                layout.addLayout(body, 28)
                layout.addStretch(1)
                ''' 页面布局 '''
                for unit in units:
                    items = self._load_setting_unit(unit)
                    for item in items:
                        if isinstance(item, list):
                            body.addWidget(self._create_group_widget(item))
                        else:
                            body.addWidget(item)
                            pass
                        pass
                    pass
                body.addStretch(3)
                # 滚动控件设置页面控件
                scroll.setWidget(page)
                # 页面控制器添加滚动控件
                self.page_controller.addWidget(scroll)
                pass
        pass

    def _load_setting_page_map(
            self, pre_index,
            units: dict[str, list[SettingUnit] | dict[str, list[SettingUnit]]]
    ) -> tuple[int, dict]:
        """ 加载设置映射列表 """
        page_map = {}
        index = pre_index
        for unit_title, unit in units.items():
            if type(unit) is dict:
                index, page_map[unit_title] = self._load_setting_page_map(index, unit)
            else:
                page_map[unit_title] = index
                index += 1
        return index, page_map

    def load_setting_units(
            self,
            units: dict[str, list[SettingUnit] | dict[str, list[SettingUnit]]]
    ):
        # 加载设置页面
        self._load_setting_pages(units)

        # 加载设置映射列表
        self.page_map.load_data(
            self._load_setting_page_map(0, units)[1]
        )
        pass

    pass
