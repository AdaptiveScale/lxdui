from pylxd.exceptions import LXDAPIException

from api.src.models.LXDModule import LXDModule

class LXCContainer(LXDModule):
    def __init__(self, input):
        self.input = input
        self.remoteHost = '127.0.0.1'
        if not self.input.get('name'):
            raise ValueError('Missing container name.')

        super(LXCContainer, self).__init__(remoteHost=self.remoteHost)

    def info(self):
        return self.client.api.containers[self.input.get('name')].get().json()['metadata']

    def create(self):
        data = {
            'name':self.input.get('name'),
            'source':{
                'type':'image',
                'alias':self.input.get('image')
            }
        }
        try:
            self.client.containers.create(data, wait=True)
            self.start()
            return self.info()
        except LXDAPIException as e:
            raise ValueError(e.response.json()['metadata']['err'] or e.response.json()['error'])

    def delete(self):
        container = self.client.containers.get(self.input.get('name'))
        #container.stop()
        try:
            container.delete()
        except LXDAPIException as e:
            raise ValueError(e.response.json()['error'])

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
