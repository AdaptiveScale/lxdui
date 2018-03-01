from api.src.models.LXDModule import LXDModule
from datetime import datetime

class LXCSnapshot(LXDModule):
    def __init__(self, input):
        self.data = {}
        if not input.get('remoteHost'):
            self.remoteHost = '127.0.0.1'
        else:
            self.remoteHost = input.get('remoteHost')

        if not input.get('name'):
            self.setSnapshot('')
        else:
            self.setSnapshot(input.get('name'))

        if input.get('container'):
            self.setContainer(input.get('container'))

        super(LXCSnapshot, self).__init__(remoteHost=self.remoteHost)


    def setSnapshot(self, input):
        self.data['name'] = input

    def setContainer(self, input):
        self.data['container'] = input


    def snapshotList(self):
        try:
            return self.client.api.containers[self.data.get('container')].snapshots.get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def snapshotInfo(self):
        try:
            return self.client.api.containers[self.data.get('container')].snapshots[self.data.get('name')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def snapshot(self):
        try:
            container = self.client.containers.get(self.data.get('container'))
            snapName = self.data.get('name')
            #snapName = '{}_{}'.format(self.data.get('container'), datetime.now().strftime('%Y-%m-%d_%H:%M'))
            container.snapshots.create(snapName)
            return self.client.api.containers[self.data.get('container')].snapshots.get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def snapshotDelete(self):
        try:
            container = self.client.containers.get(self.data.get('container'))
            container.snapshots.get(self.data.get('name')).delete()
        except Exception as e:
            raise ValueError(e)