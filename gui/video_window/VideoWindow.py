from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStyle, QSlider


class VideoWindow(QWidget):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent, Qt.Window)
        self.setWindowTitle("视频播放器")
        self.setMinimumSize(800, 600)
        # 中央窗口
        self.central_widget = QWidget(self)

        self.video = QVideoWidget(self.central_widget)
        ''' 视频控件 '''
        self.player = QMediaPlayer(self)
        ''' 播放器 '''
        self.play_list = QMediaPlaylist(self.player)
        ''' 播放列表 '''
        self.video_control = QWidget()
        ''' 视频控制控件 '''

        # self.video_control.set

        # 初始化播放器设置
        self.player.setPlaylist(self.play_list)
        self.player.setVideoOutput(self.video)
        # self.player.stateChanged.connect(self.update_play_button)
        # self.player.positionChanged.connect(self.update_position)
        # self.player.durationChanged.connect(self.update_duration)

        # 播放/暂停按钮
        self.play_btn = QPushButton()
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.toggle_play)

        # 进度条
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.sliderMoved.connect(self.player.setPosition)
        pass

    def init_ui(self):
        self.setWindowTitle("Video Player")
        layout = QVBoxLayout(self.central_widget)

        # 2. 控制栏布局
        controls_layout = QHBoxLayout()
        pass

    def toggle_play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
        pass

    def resize(self, a0):

        pass

    pass
