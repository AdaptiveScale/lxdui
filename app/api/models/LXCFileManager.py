from app.api.models.LXDModule import LXDModule
from pylxd import Client
import logging

logging = logging.getLogger(__name__)

class LXCFileManager(LXDModule):

    def __init__(self, input):
        logging.info('Connecting to LXD')
        super().__init__()
        self.input = input

    def list(self):
        pass

    def download(self):
        try:
            logging.info('Download file {} from container {}'.format(self.input.get('path'), self.input.get('name')))
            container = self.client.containers.get(self.input.get('name'))
            file = container.files.get(self.input.get('path'))
            return file
        except Exception as e:
            logging.error('Download file {} from container {} failed.'.format(self.input.get('path'), self.input.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def push(self):
        try:
            logging.info('Push file {} to container {}'.format(self.input.get('path'), self.input.get('name')))
            container = self.client.containers.get(self.input.get('name'))
            return container.files.put(self.input.get('path'), self.input.get('file'))
        except Exception as e:
            logging.error('Push file {} to container {} failed.'.format(self.input.get('path'), self.input.get('name')))
            logging.exception(e)
            raise ValueError(e)


    def delete(self):
        try:
            logging.info('Delete file {} from container {}'.format(self.input.get('path'), self.input.get('name')))
            container = self.client.containers.get(self.input.get('name'))
            return container.files.delete(self.input.get('path'))
        except Exception as e:
            logging.error('Delete file {} from container {} failed.'.format(self.input.get('path'), self.input.get('name')))
            logging.exception(e)
            raise ValueError(e)
