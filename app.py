import sys

from PyQt5.QtWidgets import QApplication

from global_manager import screen
from pyqt.qt5.window import TransparentWindow, SpritesWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用样式表确保透明
    # app.setStyleSheet("""
    #     SpritesWindow {
    #         background: transparent;
    #         border: none;
    #     }
    # """)

    window = TransparentWindow(screen.x, screen.y, screen.width, screen.height)
    window.show()
    sw = SpritesWindow(screen.x, screen.y, screen.width, screen.height)
    sw.show()
    sys.exit(app.exec_())
