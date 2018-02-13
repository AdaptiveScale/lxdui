from api.src.models.LXDModule import LXDModule

class LXCContainer(LXDModule):
    def __init__(self, input):
        self.input = input
        super.__init__(input.remoteHost)

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def move(self):
        pass

    def clone(self):
        pass

    def snapshot(self):
        pass
