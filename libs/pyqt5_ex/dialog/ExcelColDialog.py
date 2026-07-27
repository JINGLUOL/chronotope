from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from lib.pyqt5_ex import ComboBox


class ExcelColDialog(QDialog):
    def __init__(self, excel_data, target_cols: [], parent=None):
        super(ExcelColDialog, self).__init__(parent=parent)
        self.setModal(True)
        self.exe_result = None
        excel_cols = [str(col) for col in excel_data.columns]
        dialog_layout = QVBoxLayout()
        dialog_header = QHBoxLayout()
        dialog_body = QHBoxLayout()
        dialog_footer = QHBoxLayout()

        # Header
        dialog_header.addWidget(QLabel('选择对应表头以导入数据（请确保表头为表格第一行）'))
        dialog_header.setAlignment(Qt.AlignCenter)

        # Body
        combo_boxes = []
        v = QVBoxLayout()
        v.addWidget(QLabel(''))
        v.addWidget(QLabel('Excel文件表头：'))
        dialog_body.addLayout(v)
        for title in target_cols:
            v = QVBoxLayout()
            label = QLabel(title)
            label.setMinimumWidth(200)
            v.addWidget(label)
            combo_box = ComboBox()
            combo_box.addItems(excel_cols)
            combo_boxes.append(combo_box)
            v.addWidget(combo_box)
            dialog_body.addLayout(v)
            pass

        # Footer
        def dialog_close_event() -> None:
            self.close()

        def dialog_submit_event() -> None:
            # 读取Excel文件有效数据
            self.exe_result = [c.currentIndex() for c in combo_boxes]

        submit_btn = QPushButton('确定')
        cancel_btn = QPushButton('取消')
        submit_btn.clicked.connect(dialog_submit_event)
        submit_btn.clicked.connect(dialog_close_event)
        cancel_btn.clicked.connect(dialog_close_event)
        dialog_footer.addWidget(submit_btn)
        dialog_footer.addWidget(cancel_btn)
        dialog_footer.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # End
        dialog_layout.addLayout(dialog_header)
        dialog_layout.addLayout(dialog_body)
        dialog_layout.addLayout(dialog_footer)
        self.setLayout(dialog_layout)
        pass

    def exec_(self) -> list[int] | None:
        super(ExcelColDialog, self).exec_()
        return self.exe_result
