from .Law import Law


class Object(Law):

    def __init__(self, coverage):
        super().__init__()

        ''' 物体 '''
        self.coverage = coverage
        pass

    def flow(self):
        pass

    pass
