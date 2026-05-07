from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QColor, QFont, QPainter, QFontMetrics, QPixmap, QPainterPath
from PyQt5.QtWidgets import QStyledItemDelegate

from libs.c_pyqt5.tool import create_default_avatar_pixmap
from .ChatMap import ChatMap


class ChatDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ChatDelegate, self).__init__(parent)

        self.DEFAULT_PROFILE_PICTURE = create_default_avatar_pixmap()

        # 可预定义颜色、字体等
        self.self_bg_color = QColor("#95EC69")  # 自己气泡背景
        self.other_bg_color = QColor("#FFFFFF")  # 对方气泡背景
        self.text_color = QColor("#000000")
        self.time_color = QColor("#8E8E93")
        self.font = QFont("Arial", 10)
        self.time_font = QFont("Arial", 8)
        self.avatar_size = 50
        self.max_bubble_width = 330  # 最大气泡宽度（px），可根据窗口动态调整
        pass

    def paint(self, painter, option, index):
        # 从Model获取数据
        text = index.data(ChatMap.TextRole)
        is_self = index.data(ChatMap.IsSelfRole)
        avatar = None

        # 开始绘制（启用抗锯齿）
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. 绘制头像
        avatar_rect = QRect(8, option.rect.top() + 8, self.avatar_size, self.avatar_size)
        avatar = avatar or self.DEFAULT_PROFILE_PICTURE
        painter.drawPixmap(avatar_rect, avatar)

        # 2. 计算气泡矩形和文本矩形
        bubble_rect, text_rect = self.calculate_bubble_rect(option, text, is_self)

        # 3. 绘制气泡背景（圆角矩形）
        painter.setBrush(self.self_bg_color if is_self else self.other_bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(bubble_rect, 12, 12)

        # 4. 绘制文本
        painter.setFont(self.font)
        painter.setPen(self.text_color)
        painter.drawText(text_rect, Qt.TextWordWrap, text)

        # 5. 绘制时间戳（放在气泡右下角或外部，示例放在气泡下方外侧）
        # time_rect = QRect(bubble_rect.right() - 50, bubble_rect.bottom() + 2, 50, 16)
        # painter.setFont(self.time_font)
        # painter.setPen(self.time_color)
        # painter.drawText(time_rect, Qt.AlignRight | Qt.AlignTop, timestamp)

        painter.restore()
        pass

    def sizeHint(self, option, index):
        """返回每个列表项所需的大小"""
        text = index.data(ChatMap.TextRole)

        # 计算文本所需高度（给定最大宽度）
        fm = QFontMetrics(self.font)
        # 气泡最大宽度为屏幕宽度的某个比例，或固定值（可根据视图宽度动态计算）
        max_width = self.max_bubble_width
        # 计算文本矩形高度
        text_rect = fm.boundingRect(QRect(0, 0, max_width, 0), Qt.TextWordWrap, text)
        text_height = text_rect.height()

        # 气泡本身高度 = 文本高度 + 上下内边距
        bubble_height = text_height + 16
        # 整个项的高度 = 气泡高度 + 时间戳占位 + 上下边距
        total_height = max(bubble_height + 20, self.avatar_size + 16)
        # 宽度：左右预留头像和间距
        width = max(option.rect.width(), max_width + self.avatar_size + 40)
        return QSize(width, total_height)

    def calculate_bubble_rect(self, option, text, is_self):
        """根据消息来源计算气泡和文本的矩形位置"""
        avatar_left = 8
        avatar_right = option.rect.width() - self.avatar_size - 8
        spacing = 8  # 头像和气泡间距
        padding = 12  # 气泡内边距

        fm = QFontMetrics(self.font)
        # 计算文本实际需要的高度
        max_bubble_width = self.max_bubble_width
        text_rect = fm.boundingRect(QRect(0, 0, max_bubble_width - 2 * padding, 0),
                                    Qt.TextWordWrap, text)
        bubble_width = min(text_rect.width() + 2 * padding, max_bubble_width)
        bubble_height = text_rect.height() + 2 * padding

        # 根据 is_self 决定气泡位置
        if is_self:
            # 气泡靠右：头像在右，气泡在头像左边
            avatar_rect = QRect(avatar_right, option.rect.top() + 8, self.avatar_size, self.avatar_size)
            bubble_x = avatar_rect.left() - spacing - bubble_width
        else:
            # 气泡靠左：头像在左，气泡在头像右边
            avatar_rect = QRect(avatar_left, option.rect.top() + 8, self.avatar_size, self.avatar_size)
            bubble_x = avatar_rect.right() + spacing

        bubble_y = option.rect.top() + 8
        bubble_rect = QRect(bubble_x, bubble_y, bubble_width, bubble_height)

        # 文本矩形（气泡内部）
        text_rect = QRect(bubble_rect.x() + padding, bubble_rect.y() + padding,
                          bubble_width - 2 * padding, bubble_height - 2 * padding)
        return bubble_rect, text_rect

    pass
