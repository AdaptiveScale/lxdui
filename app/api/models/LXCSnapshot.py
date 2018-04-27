from app.api.models.LXDModule import LXDModule
from app.api.utils.snapshotMapper import getSnapshotData

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

        if input.get('newContainer'):
            self.setNewContainer(input.get('newContainer'))

        super(LXCSnapshot, self).__init__(remoteHost=self.remoteHost)


    def setSnapshot(self, input):
        self.data['name'] = input

    def setContainer(self, input):
        self.data['container'] = input

    def setNewContainer(self, input):
        self.data['newContainer'] = input


    def snapshotList(self):
        try:
            container = self.client.containers.get(self.data.get('container'))
            result = []
            for snap in container.snapshots.all():
                result.append(getSnapshotData(snap))

            return result
        except Exception as e:
            raise ValueError(e)

    def snapshotInfo(self):
        try:
            return self.client.api.containers[self.data.get('container')].snapshots[self.data.get('name')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def snapshot(self, s=False):
        try:
            container = self.client.containers.get(self.data.get('container'))
            snapName = self.data.get('name')
            if self._checkSnapshot(container) == False:
                raise ValueError('Snapshot with name {} already exists.'.format(snapName))
            container.snapshots.create(snapName, stateful=s, wait=True)
            return self.client.api.containers[self.data.get('container')].snapshots.get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def snapshotDelete(self):
        try:
            container = self.client.containers.get(self.data.get('container'))
            container.snapshots.get(self.data.get('name')).delete()
        except Exception as e:
            raise ValueError(e)


    def snapshotRestore(self):
        try:
            return self.client.api.containers[self.data.get('container')].put(json={'restore': self.data.get('name')}).json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def snapshotPublish(self):
        try:
            container = self.client.containers.get(self.data.get('container'))
            image = container.snapshots.get(self.data.get('name')).publish(wait=True)
            image.add_alias(self.data.get('name'), self.data.get('name'))
            return self.client.api.images[image.fingerprint].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def snapshotCreateContainer(self):
        try:
            container = self.client.containers.get(self.data.get('container'))
            image = container.snapshots.get(self.data.get('name')).publish(wait=True)
            image.add_alias(self.data.get('name'), self.data.get('name'))
            config = {'name': self.data.get('newContainer'), 'source': {'type': 'image', 'alias': self.data.get('name')}}
            self.client.containers.create(config, wait=True)

            newImage = self.client.images.get(image.fingerprint)
            newImage.delete(wait=True)

        except Exception as e:
            raise ValueError(e)

    def _checkSnapshot(self, container):
        for snap in container.snapshots.all():
            if snap.name == self.data.get('name'):
                return False

        return True
