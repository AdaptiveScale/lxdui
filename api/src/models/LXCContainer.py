from api.src.models.LXDModule import LXDModule

class LXCContainer(LXDModule):
    def __init__(self, input):
        self.input = input
        self.remoteHost = '127.0.0.1'
        if not self.input.get('name'):
            raise ValueError('Missing container name.')

        super(LXCContainer, self).__init__(remoteHost=self.remoteHost)

    def info(self):
        try:
            return self.client.api.containers[self.input.get('name')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

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
        except Exception as e:
            raise ValueError(e.response.json()['metadata']['err'] or e.response.json()['error'])

    def delete(self):
        try:
            container = self.client.containers.get(self.input.get('name'))
            container.delete()
        except Exception as e:
            raise ValueError(e)

    def update(self):
        pass

    def start(self):
        try:
            container = self.client.containers.get(self.input.get('name'))
            container.start()
        except Exception as e:
            raise ValueError(e)

    def stop(self):
        try:
            container = self.client.containers.get(self.input.get('name'))
            container.stop()
        except Exception as e:
            raise ValueError(e)

    def restart(self):
        try:
            container = self.client.containers.get(self.input.get('name'))
            container.restart()
        except:
            raise ValueError(e)

    def move(self):
        pass

    def clone(self):
        pass

    def snapshot(self):
        try:
            container = self.client.containers.get(self.input.get('name'))
            return container.snapshots.all()
        except Exception as e:
            raise ValueError(e)
