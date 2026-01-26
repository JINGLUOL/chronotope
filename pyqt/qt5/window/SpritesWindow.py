from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QBrush, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from sprite import SpriteAbs
from sprite.hollow_knight import KnightSprite


class SpritesWindow(QGraphicsView):
    def __init__(self, x, y, w, h):
        super(SpritesWindow, self).__init__()
        self.setGeometry(x, y, w, h)

        # 设置窗口标识
        self.setWindowFlags(
            Qt.Window |
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        # 设置框架样式为无
        self.setFrameShape(QGraphicsView.NoFrame)

        # 设置视口（Viewport）透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState)

        # 创建场景
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(Qt.transparent))
        self.setScene(self.scene)

        # 设置渲染优化
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportUpdateMode(self.FullViewportUpdate)  # 减少闪烁

        # 精灵列表
        self.sprites: list[SpriteAbs] = []
        self.create_knight_sprite()

        self.time_counter = 0
        self.delay: int = 16

        # 游戏循环
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(self.delay)  # 60FPS

        # 帧率计算
        self.frame_count = 0
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(1000)
        pass

    def _time_counter_increment(self):
        self.time_counter += self.delay

    def _add_sprite(self, sprite: SpriteAbs):
        self.sprites.append(sprite)
        self.scene.addItem(sprite)
        pass

    def create_knight_sprite(self):
        sprite = KnightSprite()
        self._add_sprite(sprite)
        pass

    def game_loop(self):
        # scene_rect = self.scene.sceneRect()

        # 更新所有精灵
        for sprite in self.sprites:
            sprite.update_anim(self.time_counter)
            sprite.sprite_behavior_handle()

        self._time_counter_increment()
        self.frame_count += 1

    def update_fps(self):
        # print(f"FPS: {self.frame_count}")
        self.frame_count = 0
        pass

    def paintEvent(self, event):
        """重写paintEvent确保透明背景绘制"""
        # 先清空背景
        painter = QPainter(self.viewport())
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(event.rect(), Qt.transparent)
        painter.end()

        # 调用父类的绘制
        super().paintEvent(event)
        pass

    pass
