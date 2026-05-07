class Law:

    def __init__(self, create_timestamp: float):
        """ 初始化参数 """

        ''' 空间 '''
        self.position: list = [0, 0, 0]
        """ 坐标 """
        self.velocity: list = [0, 0, 0]
        """ 受力 """
        self.rotation_angles: list = [0, 0, 0]
        """ 旋转角度 """
        self.rotation_speed: float = 0
        """ 旋转速度 """

        ''' 时间 '''
        self.start_timestamp: float = create_timestamp
        """ 创建时间 """
        self.timestamp: float = create_timestamp
        """ 更新时间 """
        pass

    pass
