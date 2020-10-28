from app.api.models.LXDModule import LXDModule
from app.api.utils.snapshotMapper import getSnapshotData
import logging

logging = logging.getLogger(__name__)

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

        logging.info('Connecting to LXD')
        super(LXCSnapshot, self).__init__(remoteHost=self.remoteHost)


    def setSnapshot(self, input):
        logging.debug('Setting snapshot name to {}'.format(input))
        self.data['name'] = input

    def setContainer(self, input):
        logging.debug('Setting snapshot container to {}'.format(input))
        self.data['container'] = input

    def setNewContainer(self, input):
        logging.debug('Setting snapshot newContainer to {}'.format(input))
        self.data['newContainer'] = input


    def snapshotList(self):
        try:
            logging.info('Reading snapshot list for container {}'.format(self.data.get('container')))
            container = self.client.instances.get(self.data.get('container'))
            result = []
            for snap in container.snapshots.all():
                result.append(getSnapshotData(snap))

            return result
        except Exception as e:
            logging.error('Failed to retrieve snapshot list for container {}'.format(self.data.get('container')))
            logging.exception(e)
            raise ValueError(e)

    def snapshotInfo(self):
        try:
            logging.info('Reading snapshot {} info for container {}'.format(self.data.get('name'), self.data.get('container')))
            return self.client.api.instances[self.data.get('container')].snapshots[self.data.get('name')].get().json()['metadata']
        except Exception as e:
            logging.error('Failed to retrieve snapshot {} info for container {}'.format(self.data.get('name'), self.data.get('container')))
            logging.exception(e)
            raise ValueError(e)

    def snapshot(self, s=False):
        try:
            logging.info(
                'Creating snapshot {} for container {}'.format(self.data.get('name'), self.data.get('container')))
            container = self.client.instances.get(self.data.get('container'))
            snapName = self.data.get('name')
            if self._checkSnapshot(container) == False:
                logging.error('Failed to create snapshot {}. Snapshot with name {} already exists.'.format(self.data.get('name'), snapName))
                raise ValueError('Snapshot with name {} already exists.'.format(snapName))
            container.snapshots.create(snapName, stateful=s, wait=True)
            return self.client.api.instances[self.data.get('container')].snapshots.get().json()['metadata']
        except Exception as e:
            logging.error('Failed to create snapshot {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def snapshotDelete(self):
        try:
            logging.info('Deleting snapshot {} for container {}'.format(self.data.get('name'), self.data.get('container')))
            container = self.client.instances.get(self.data.get('container'))
            container.snapshots.get(self.data.get('name')).delete()
        except Exception as e:
            logging.error('Failed to delete snapshot {} for container {}'.format(self.data.get('name'), self.data.get('container')))
            logging.exception(e)
            raise ValueError(e)


    def snapshotRestore(self):
        try:
            logging.info(
                'Restoring snapshot {} for container {}'.format(self.data.get('name'), self.data.get('container')))
            return self.client.api.instances[self.data.get('container')].put(json={'restore': self.data.get('name')}).json()['metadata']
        except Exception as e:
            logging.error('Failed to restore snapshot {} for container {}'.format(self.data.get('name'),
                                                                                 self.data.get('container')))
            logging.exception(e)
            raise ValueError(e)

    def snapshotPublish(self):
        try:
            logging.info(
                'Publishing snapshot {} for container {}'.format(self.data.get('name'), self.data.get('container')))
            container = self.client.instances.get(self.data.get('container'))
            image = container.snapshots.get(self.data.get('name')).publish(wait=True)
            image.add_alias(self.data.get('name'), self.data.get('name'))
            return self.client.api.images[image.fingerprint].get().json()['metadata']
        except Exception as e:
            logging.error('Failed to publish snapshot {} for container {}'.format(self.data.get('name'),
                                                                                  self.data.get('container')))
            logging.exception(e)
            raise ValueError(e)

    def snapshotCreateContainer(self):
        try:
            logging.info(
                'Creating container {} from snapshot {}'.format(self.data.get('newContainer'), self.data.get('name')))
            container = self.client.instances.get(self.data.get('container'))
            image = container.snapshots.get(self.data.get('name')).publish(wait=True)
            image.add_alias(self.data.get('name'), self.data.get('name'))
            config = {'name': self.data.get('newContainer'), 'source': {'type': 'image', 'alias': self.data.get('name')}}
            self.client.instances.create(config, wait=True)

            newImage = self.client.images.get(image.fingerprint)
            newImage.delete(wait=True)

        except Exception as e:
            logging.error('Failed to create container {} from snapshot {}'.format(self.data.get('newContainer'), self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def _checkSnapshot(self, container):
        logging.info(
            'Check if snapshot {} exists'.format(self.data.get('name')))
        for snap in container.snapshots.all():
            if snap.name == self.data.get('name'):
                return False

        return True
