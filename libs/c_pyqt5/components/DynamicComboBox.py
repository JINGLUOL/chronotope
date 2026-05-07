from typing import Callable

from PyQt5.QtWidgets import QComboBox


class DynamicComboBox(QComboBox):

    def __init__(self, fetch_data: Callable[[], list[str]], parent=None):
        super().__init__(parent)
        self.fetch_data = fetch_data
        # 可选：初始时加载一次数据
        self.reload_items()
        pass

    def reload_items(self):
        """自定义的数据加载逻辑：清空并重新添加列表项"""
        # 保存当前选中的文本（可选，用于恢复）
        current_text = self.currentText()

        # 清空现有项
        self.clear()

        # 模拟从数据库或网络获取新数据
        new_items = self.fetch_data()  # 你的数据获取函数

        # 添加新项
        self.addItems(new_items)

        # 尝试恢复之前选中的项（若数据中存在）
        index = self.findText(current_text)
        if index >= 0:
            self.setCurrentIndex(index)
        elif self.count() > 0:
            self.setCurrentIndex(0)  # 或保留空白
        pass

    def showPopup(self):
        """重写：点击下拉箭头时先刷新数据，再显示下拉列表"""
        # ① 执行数据刷新（重新加载列表项）
        self.reload_items()

        # ② 调用父类的 showPopup，显示下拉列表
        super().showPopup()
        pass

    pass
