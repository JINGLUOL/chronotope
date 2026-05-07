from dataclasses import dataclass

from PyQt5.QtCore import Qt


@dataclass
class ChatMap:
    TextRole = Qt.DisplayRole
    SenderRole = Qt.UserRole + 1
    TimestampRole = Qt.UserRole + 2
    AvatarRole = Qt.UserRole + 3
    IsSelfRole = Qt.UserRole + 4
