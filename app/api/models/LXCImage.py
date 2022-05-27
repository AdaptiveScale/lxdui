from app.api.models.LXDModule import LXDModule
from app.lib.conf import MetaConf
from app.api.utils.firebaseAuthentication import firebaseLogin
from app import __metadata__ as meta
import logging
import requests
import subprocess
import shutil
import os
import yaml
import tarfile

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
    def exportImage(self, input, logo=None):
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
                input['image'] = '{}.tar.gz'.format(self.data.get('fingerprint'))
            if os.path.exists('{}.tar.xz'.format(self.data.get('fingerprint'))):
                shutil.move('{}.tar.xz'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['image'] = '{}.tar.xz'.format(self.data.get('fingerprint'))
            if os.path.exists('{}.squashfs'.format(self.data.get('fingerprint'))):
                shutil.move('{}.squashfs'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['image'] = '{}.squashfs'.format(self.data.get('fingerprint'))
            if os.path.exists('meta-{}.tar.gz'.format(self.data.get('fingerprint'))):
                shutil.move('meta-{}.tar.gz'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['metadata'] = 'meta-{}.tar.gz'.format(self.data.get('fingerprint'))
            if os.path.exists('meta-{}.tar.xz'.format(self.data.get('fingerprint'))):
                shutil.move('meta-{}.tar.xz'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['metadata'] = 'meta-{}.tar.xz'.format(self.data.get('fingerprint'))
            if os.path.exists('meta-{}.tar.xz'.format(self.data.get('fingerprint'))):
                shutil.move('meta-{}.squashfs'.format(self.data.get('fingerprint')), 'tmp/images/{}/'.format(self.data.get('fingerprint')))
                input['metadata'] = 'meta-{}.squashfs'.format(self.data.get('fingerprint'))

            #Prepare & Move the yaml file
            self.prepareImageYAML(input)
            shutil.move('image.yaml', 'tmp/images/{}/'.format(self.data.get('fingerprint')))

            #TODO Prepare README.md
            file = open('tmp/images/{}/README.md'.format(self.data.get('fingerprint')), 'a')
            file.write('#README\n')
            file.write(input.get('documentation'))
            file.close()

            #TODO Prepare Logo
            if logo:
                logo.save('tmp/images/{}/{}'.format(self.data.get('fingerprint'), 'logo.png'))

            return MetaConf().getConfRoot() + '/tmp/images/{}'.format(self.data.get('fingerprint'))
        except Exception as e:
            logging.error('Failed to export the image {}'.format(self.data.get('fingerprint')))
            logging.exception(e)
            raise ValueError(e)

    def prepareImageYAML(self, input):
        if input.get('metadata') == None: input['metadata'] = ''
        data = {
            'title': input.get('imageAlias', ''),
            'description': input.get('imageDescription', ''),
            'author': {
                'name': input.get('authorName', ''),
                'alias': '',
                'email': input.get('authorEmail', '')
            },
            'license': input.get('license', ''),
            'readme': 'README.md',
            'tags': input.get('imageTags').split(','),
            'logo': 'logo.png',
            'image': input.get('image'),
            'metadata': input.get('metadata'),
            'fingerprint': self.data.get('fingerprint'),
            'public': True
        }

        data.update(self.client.api.images[self.data.get('fingerprint')].get().json()['metadata'])

        with open('image.yaml', 'w') as yamlFile:
            yaml.dump(data, yamlFile, default_flow_style=False)


    def pushImage(self, input):
        try:
            #Login
            result = firebaseLogin(input.get('username'), input.get('password'))
            if result.ok:
                token = result.json()['idToken']
            else:
                raise ValueError('Login failed: {}'.format(result.json()['error']['message']))

            self.data['fingerprint'] = self.client.images.get(self.data.get('fingerprint')).fingerprint

            if os.path.exists('tmp/images/{}'.format(self.data.get('fingerprint'))):
                logging.info('Image exists. Ready for push.')
                print ("Image exists. Ready for push.")

                #Prepare the files for upload.
                with open('tmp/images/{}/image.yaml'.format(self.data.get('fingerprint'))) as stream:
                    yamlData = yaml.safe_load(stream)

                files = {
                    'yaml': open('tmp/images/{}/image.yaml'.format(self.data.get('fingerprint')), 'rb')
                }

                headers = {'Authorization': token}

                response = requests.post('{}/cliAddPackage'.format(meta.IMAGE_HUB), headers=headers, files=files, data={'id': self.data.get('fingerprint')})

                if response.ok == False:
                    logging.error('Failed to push the image {}'.format(self.data.get('fingerprint')))
                    raise ValueError(response.json()['message'])

                print("yaml uploaded successfully.")

                print("Uploading:")
                for file in response.json()['filesRequired']:
                    for key in file:
                        files = {}
                        if file[key] != '':
                            if os.path.exists('tmp/images/{}/{}'.format(self.data.get('fingerprint'), file[key])):
                                files['file'] = open('tmp/images/{}/{}'.format(self.data.get('fingerprint'), file[key]), 'rb')
                                requests.post('{}/cliAddFile'.format(meta.IMAGE_HUB), headers=headers, files=files, data={'id': self.data.get('fingerprint')}).json()
                                print('File {} uploaded successfully'.format(file[key]))
                            else:
                                print('File {} does not exist'.format(file[key]))

            else:
                logging.error('Failed to push the image {}'.format(self.data.get('fingerprint')))
                logging.exception('Image is not prepared. Please prepare the image using the command lxdui image prep <fingerprint>')
                raise ValueError('Image is not prepared. Please prepare the image using the command: lxdui image prep <fingerprint>')

        except Exception as e:
            logging.error('Failed to push the image {}'.format(self.data.get('fingerprint')))
            logging.exception(e)
            raise ValueError(e)


    def importImage(self, input):

        logging.info('Importing image {}'.format(self.data.get('fingerprint')))

        shutil.rmtree('tmp/downloaded/{}/'.format(self.data.get('fingerprint')), ignore_errors=True)
        os.makedirs('tmp/downloaded/{}'.format(self.data.get('fingerprint')), exist_ok=True)

        # Download and extract the file
        r = requests.get('{}/cliDownloadRepo/{}'.format(meta.IMAGE_HUB, self.data.get('fingerprint')), stream=True)
        with open('tmp/downloaded/{}/package.tar.gz'.format(self.data.get('fingerprint')), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        tfile = tarfile.open('tmp/downloaded/{}/package.tar.gz'.format(self.data.get('fingerprint')), 'r:gz')
        tfile.extractall('tmp/downloaded/{}/'.format(self.data.get('fingerprint')))

        with open('tmp/downloaded/{}/image.yaml'.format(self.data.get('fingerprint'))) as stream:
            yamlData = yaml.safe_load(stream)


        if os.path.exists("tmp/downloaded/{0}/meta-{0}.tar.xz".format(self.data.get('fingerprint'))) and os.path.exists("tmp/downloaded/{0}/{0}.tar.xz".format(self.data.get('fingerprint'))):
            p2 = subprocess.Popen(["lxc", "image", "import",
                               "tmp/downloaded/{0}/meta-{0}.tar.xz".format(self.data.get('fingerprint')),
                               "tmp/downloaded/{0}/{0}.tar.xz".format(self.data.get('fingerprint'))], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

        elif os.path.exists("tmp/downloaded/{0}/meta-{0}.tar.gz".format(self.data.get('fingerprint'))) and os.path.exists("tmp/downloaded/{0}/{0}.tar.gz".format(self.data.get('fingerprint'))):
            p2 = subprocess.Popen(["lxc", "image", "import",
                               "tmp/downloaded/{0}/meta-{0}.tar.gz".format(self.data.get('fingerprint')),
                               "tmp/downloaded/{0}/{0}.tar.gz".format(self.data.get('fingerprint'))], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

        elif os.path.exists("tmp/downloaded/{0}/meta-{0}.tar.gz".format(self.data.get('fingerprint'))) == False and os.path.exists("tmp/downloaded/{0}/{0}.tar.gz".format(self.data.get('fingerprint'))):
            p2 = subprocess.Popen(["lxc", "image", "import",
                               "tmp/downloaded/{0}/{0}.tar.gz".format(self.data.get('fingerprint'))], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

        elif os.path.exists("tmp/downloaded/{0}/meta-{0}.tar.xz".format(self.data.get('fingerprint'))) == False and os.path.exists("tmp/downloaded/{0}/{0}.tar.gz".format(self.data.get('fingerprint'))):
            p2 = subprocess.Popen(["lxc", "image", "import",
                               "tmp/downloaded/{0}/{0}.tar.xz".format(self.data.get('fingerprint'))], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

        elif os.path.exists("tmp/downloaded/{0}/meta-{0}.tar.xz".format(self.data.get('fingerprint'))) == False and os.path.exists("tmp/downloaded/{0}/{0}.squashfs".format(self.data.get('fingerprint'))):
            p2 = subprocess.Popen(["lxc", "image", "import",
                               "tmp/downloaded/{0}/{0}.squashfs".format(self.data.get('fingerprint'))], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

        elif os.path.exists("tmp/downloaded/{0}/meta-{0}.tar.xz".format(self.data.get('fingerprint'))) and os.path.exists("tmp/downloaded/{0}/{0}.squashfs".format(self.data.get('fingerprint'))):
            p2 = subprocess.Popen(["lxc", "image", "import",
                                "tmp/downloaded/{0}/meta-{0}.tar.xz".format(self.data.get('fingerprint')),
                                "tmp/downloaded/{0}/{0}.squashfs".format(self.data.get('fingerprint'))], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

        elif os.path.exists("tmp/downloaded/{0}/meta-{0}.squashfs".format(self.data.get('fingerprint'))) and os.path.exists("tmp/downloaded/{0}/{0}.squashfs".format(self.data.get('fingerprint'))):
            p2 = subprocess.Popen(["lxc", "image", "import",
                                "tmp/downloaded/{0}/meta-{0}.squashfs".format(self.data.get('fingerprint')),
                                "tmp/downloaded/{0}/{0}.squashfs".format(self.data.get('fingerprint'))], stdout=subprocess.PIPE)
            output_rez = p2.stdout.read()

        shutil.rmtree('tmp/downloaded/{}/'.format(self.data.get('fingerprint')), ignore_errors=True)

        image = self.client.images.get(self.data.get('fingerprint'))
        image.add_alias(yamlData['title'], yamlData['title'])

        # self.client.images.create(image_data='tmp/images/394986c986a778f64903fa043a3e280bda41e4793580b22c5d991ec948ced6dd/394986c986a778f64903fa043a3e280bda41e4793580b22c5d991ec948ced6dd.tar.xz',
        #                           metadata='tmp/images/394986c986a778f64903fa043a3e280bda41e4793580b22c5d991ec948ced6dd/meta-394986c986a778f64903fa043a3e280bda41e4793580b22c5d991ec948ced6dd.tar.xz')


    def listHub(self, input):
        try:
            logging.info('Listing images')
            output = "# | Title | Fingerprint | OS | Author\n"

            result = requests.get('{}/cliListRepos'.format(meta.IMAGE_HUB))

            i = 1
            for r in result.json():
                output += '{} | {} | {} | {} | {}\n'.format(i, r['title'], r['fingerprint'], r['properties'].get('name'), r['author']['name'])
                i+=1

            return output
        except Exception as e:
            logging.error('Failed to list images from kuti.io')
            logging.exception(e)
            raise ValueError(e)