from api.src.models.LXDModule import LXDModule

class LXCContainer(LXDModule):
    def __init__(self, input):
        self.input = input
        self.remoteHost = '127.0.0.1'
        if not self.input.get('name'):
            raise ValueError('Missing container name.')
        if 'remoteHost' in self.input:
            self.remoteHost = self.input.get('remoteHost')

        super(LXCContainer, self).__init__(remoteHost=self.remoteHost)

    def info(self):
        return self.client.api.containers[self.input.get('name')].get().json()

    def create(self):
        pass

    def delete(self):
        container = self.client.containers.get(self.input.get('name'))
        #container.stop()
        container.delete()

    def update(self):
        pass

    def start(self):
        container = self.client.containers.get(self.input.get('name'))
        container.start()

    def stop(self):
        container = self.client.containers.get(self.input.get('name'))
        container.stop()

    def restart(self):
        container = self.client.containers.get(self.input.get('name'))
        container.restart()

    def move(self):
        pass

    def clone(self):
        pass

    def snapshot(self):
        container = self.client.containers.get(self.input.get('name'))
        return container.snapshots.all()
