from app.api.models.LXDModule import LXDModule
import logging
import subprocess
import shutil
import os
import yaml

logging = logging.getLogger(__name__)

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
            logging.error('Failed to retrieve information for image {}'.format(self.data.get('fingerprint')))
            logging.exception(e)
            raise ValueError(e)

    def deleteImage(self):
        try:
            logging.info('Deleting image {}'.format(self.data.get('fingerprint')))
            image = self.client.images.get(self.data.get('fingerprint'))
            image.delete()
        except Exception as e:
            logging.error('Failed to delete the image {}'.format(self.data.get('fingerprint')))
            logging.exception(e)
            raise ValueError(e)

    #TODO Refactor this part
    def exportImage(self, input):
        try:
            logging.info('Exporting image {}'.format(self.data.get('fingerprint')))
            p2 = subprocess.Popen(["lxc", "image", "export", self.data.get('fingerprint')], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

            #Make dir for the export
            shutil.rmtree('tmp/{}/'.format(self.data.get('fingerprint')), ignore_errors=True)
            os.makedirs('tmp/{}'.format(self.data.get('fingerprint')), exist_ok=True)

            #Move the export - Check for both extenstion .tar.gz & .tar.xz
            if os.path.exists('{}.tar.gz'.format(self.data.get('fingerprint'))):
                shutil.move('{}.tar.gz'.format(self.data.get('fingerprint')), 'tmp/{}/'.format(self.data.get('fingerprint')))
                input['image'] = 'tmp/{0}/{0}.tar.gz'.format(self.data.get('fingerprint'))
            if os.path.exists('{}.tar.xz'.format(self.data.get('fingerprint'))):
                shutil.move('{}.tar.xz'.format(self.data.get('fingerprint')), 'tmp/{}/'.format(self.data.get('fingerprint')))
                input['image'] = 'tmp/{0}/{0}.tar.xz'.format(self.data.get('fingerprint'))
            if os.path.exists('meta-{}.tar.gz'.format(self.data.get('fingerprint'))):
                shutil.move('meta-{}.tar.gz'.format(self.data.get('fingerprint')), 'tmp/{}/'.format(self.data.get('fingerprint')))
                input['metadata'] = 'tmp/{0}/meta-{0}.tar.gz'.format(self.data.get('fingerprint'))
            if os.path.exists('meta-{}.tar.xz'.format(self.data.get('fingerprint'))):
                shutil.move('meta-{}.tar.xz'.format(self.data.get('fingerprint')), 'tmp/{}/'.format(self.data.get('fingerprint')))
                input['metadata'] = 'tmp/{0}/meta-{0}.tar.xz'.format(self.data.get('fingerprint'))

            #Prepare & Move the yaml file
            self.prepareImageYAML(input)
            shutil.move('{}.yaml'.format(self.data.get('fingerprint')), 'tmp/{}/'.format(self.data.get('fingerprint')))

            #TODO Prepare README.md

            #TODO Prepare Logo

            return output_rez
        except Exception as e:
            logging.error('Failed to export the image {}'.format(self.data.get('fingerprint')))
            logging.exception(e)
            raise ValueError(e)

    def prepareImageYAML(self, input):
        if input.get('metadata') == None: input['metadata'] = ''
        data = {
            'title': 'Wordpress 15.1',
            'description': 'Some description',
            'author': {
                'name': 'AdaptiveScale',
                'alias': 'as',
                'email': 'info@adaptivescale.com'
            },
            'license': 'MIT',
            'readme': 'README.md',
            'tags': ['nginx', 'redis', 'python3', 'flask'],
            'image': input.get('image'),
            'metadata': input.get('metadata')
        }

        data.update(self.client.api.images[self.data.get('fingerprint')].get().json()['metadata'])

        with open('{}.yaml'.format(self.data.get('fingerprint')), 'w') as yamlFile:
            yaml.dump(data, yamlFile, default_flow_style=False)