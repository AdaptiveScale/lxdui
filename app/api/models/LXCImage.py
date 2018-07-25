from app.api.models.LXDModule import LXDModule
from app.lib.conf import MetaConf
import logging
import requests
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
            #Check if image exists & Update the fingerprint with the full fingerprint
            self.data['fingerprint'] = self.client.images.get(self.data.get('fingerprint')).fingerprint

            logging.info('Exporting image {}'.format(self.data.get('fingerprint')))
            p2 = subprocess.Popen(["lxc", "image", "export", self.data.get('fingerprint')], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

            #Make dir for the export
            shutil.rmtree('tmp/images/{}/'.format(self.data.get('fingerprint')), ignore_errors=True)
            os.makedirs('tmp/images/{}'.format(self.data.get('fingerprint')), exist_ok=True)

            #Move the export - Check for both extenstion .tar.gz & .tar.xz
            if os.path.exists('{}.tar.gz'.format(self.data.get('fingerprint'))):
                shutil.move('{}.tar.gz'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['image'] = 'tmp/images/{0}/{0}.tar.gz'.format(self.data.get('fingerprint'))
            if os.path.exists('{}.tar.xz'.format(self.data.get('fingerprint'))):
                shutil.move('{}.tar.xz'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['image'] = 'tmp/images/{0}/{0}.tar.xz'.format(self.data.get('fingerprint'))
            if os.path.exists('meta-{}.tar.gz'.format(self.data.get('fingerprint'))):
                shutil.move('meta-{}.tar.gz'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['metadata'] = 'tmp/images/{0}/meta-{0}.tar.gz'.format(self.data.get('fingerprint'))
            if os.path.exists('meta-{}.tar.xz'.format(self.data.get('fingerprint'))):
                shutil.move('meta-{}.tar.xz'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['metadata'] = 'tmp/images/{0}/meta-{0}.tar.xz'.format(self.data.get('fingerprint'))

            #Prepare & Move the yaml file
            self.prepareImageYAML(input)
            shutil.move('{}.yaml'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))

            #TODO Prepare README.md
            open('tmp/images/{}/README.md'.format(self.data.get('fingerprint')), 'a').close()

            #TODO Prepare Logo

            return MetaConf().getConfRoot() + '/tmp/images/{}'.format(self.data.get('fingerprint'))
        except Exception as e:
            logging.error('Failed to export the image {}'.format(self.data.get('fingerprint')))
            logging.exception(e)
            raise ValueError(e)

    def prepareImageYAML(self, input):
        if input.get('metadata') == None: input['metadata'] = ''
        data = {
            'title': '',
            'description': '',
            'author': {
                'name': '',
                'alias': '',
                'email': ''
            },
            'license': '',
            'readme': 'tmp/images/{}/README.md'.format(self.data.get('fingerprint')),
            'tags': [],
            'logo': 'tmp/images/{}/logo.png'.format(self.data.get('fingerprint')),
            'image': input.get('image'),
            'metadata': input.get('metadata'),
            'fingerprint': self.data.get('fingerprint')
        }

        data.update(self.client.api.images[self.data.get('fingerprint')].get().json()['metadata'])

        with open('{}.yaml'.format(self.data.get('fingerprint')), 'w') as yamlFile:
            yaml.dump(data, yamlFile, default_flow_style=False)


    def pushImage(self, input):
        try:
            self.data['fingerprint'] = self.client.images.get(self.data.get('fingerprint')).fingerprint

            if os.path.exists('tmp/images/{}'.format(self.data.get('fingerprint'))):
                logging.info('Image exists. Ready for push.')
                print ("Image exists. Ready for push.")

                #Prepare the files for upload.
                with open('tmp/images/{0}/{0}.yaml'.format(self.data.get('fingerprint'))) as stream:
                    yamlData = yaml.load(stream)

                files = {
                    'yaml': open('tmp/images/{0}/{0}.yaml'.format(self.data.get('fingerprint'), 'rb'))
                }

                response = requests.post('http://postma-echo.com/post', files=files).json()

                print (response)

                return True

                files = {
                    'image': open(yamlData['image'], 'rb'),
                    'meta-image': open(yamlData['metadata'], 'rb'),
                    'readme': open(yamlData['readme'], 'rb'),
                    # 'logo': open(yamlData['logo'], 'rb')
                }

                r = requests.post('http://postma-echo.com/post', files=files)
            else:
                logging.error('Failed to push the image {}'.format(self.data.get('fingerprint')))
                logging.exception('Image is not prepared. Please prepare the image using the command lxdui image prep <fingerprint>')
                raise ValueError('Image is not prepared. Please prepare the image using the command: lxdui image prep <fingerprint>')

        except Exception as e:
            logging.error('Failed to push the image {}'.format(self.data.get('fingerprint')))
            logging.exception(e)
            raise ValueError(e)
