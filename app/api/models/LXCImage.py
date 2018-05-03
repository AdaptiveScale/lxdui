from app.api.models.LXDModule import LXDModule
import logging

class LXCImage(LXDModule):
    def __init__(self, input):
        self.data = {}
        if not input.get('remoteHost'):
            self.remoteHost = '127.0.0.1'
        else:
            self.remoteHost = input.get('remoteHost')

        if not input.get('fingerprint'):
            logging.error('Image fingerprint is required for any image operation')
            raise ValueError('Missing image fingerprint.')

        self.setFingerprint(input.get('fingerprint'))

        if input.get('image'):
            self.setImage(input.get('image'))

        logging.info('Connecting to LXD')
        super(LXCImage, self).__init__(remoteHost=self.remoteHost)


    def setAlias(self, input):
        logging.debug('Setting image alias to {}'.format(input))
        self.data['alias'] = input

    def setFingerprint(self, input):
        logging.debug('Setting image fingerprint to {}'.format(input))
        self.data['fingerprint'] = input

    def setImage(self, input):
        logging.debug('Setting image to {}'.format(input))
        self.data['image'] = input

    def getImage(self):
        try:
            logging.info('Reading image {} details'.format(self.data.get('fingerprint')))
            return self.client.api.images[self.data.get('fingerprint')].get().json()['metadata']
        except Exception as e:
            logging.error('Failed to retrieve information for image {}'.format(self.data.get('fingerprint')), e)
            raise ValueError(e)

    def deleteImage(self):
        try:
            logging.info('Deleting image {}'.format(self.data.get('fingerprint')))
            image = self.client.images.get(self.data.get('fingerprint'))
            image.delete()
        except Exception as e:
            logging.error('Failed to delete the image {}'.format(self.data.get('fingerprint')), e)
            raise ValueError(e)