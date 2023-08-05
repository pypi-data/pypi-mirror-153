class BatchManager(object):

    def __init__(self):
        self.actions = []

    def register(self, action):
        self.actions.append(action)

    def __call__(self, *args, **kwargs):
        self.run()

    def run(self):
        for action in self.actions:
            action()

        self.actions = []
