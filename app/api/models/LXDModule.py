from app.api.models.Base import Base
from app.api.utils.remoteImageMapper import remoteImagesList
from app.lib.conf import Config
from app import __metadata__ as meta

from pylxd import Client
import requests
import logging

logging = logging.getLogger(__name__)

class LXDModule(Base):
    # Default 127.0.0.1 -> Move to Config
    def __init__(self, remoteHost='127.0.0.1'):

        conf = Config()
        logging.info('Accessing PyLXD client')
        try:
            remoteHost = Config().get(meta.APP_NAME, '{}.lxd.remote'.format(meta.APP_NAME.lower()))
            sslKey = conf.get(meta.APP_NAME, '{}.ssl.key'.format(meta.APP_NAME.lower()))
            sslCert = conf.get(meta.APP_NAME, '{}.ssl.cert'.format(meta.APP_NAME.lower()))
            sslVerify = conf.get(meta.APP_NAME, '{}.lxd.sslverify'.format(meta.APP_NAME.lower()))

            if sslVerify.lower in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']:
                sslVerify = True
            else:
                sslVerify = False

            self.client = Client(endpoint=remoteHost,
                cert=(sslCert, sslKey), verify=sslVerify)
        except:
            logging.info('using local socket')
            self.client = Client()




    def listContainers(self):
        try:
            logging.info('Reading container list')
            return self.client.containers.all()
        except Exception as e:
            logging.error('Failed to read container list: ')
            logging.exception(e)
            raise ValueError(e)

    def listLocalImages(self):
        try:
            logging.info('Reading local image list')
            results = []
            for image in self.client.api.images.get().json()['metadata']:
                results.append(self.client.api.images[image.split('/')[-1]].get().json()['metadata'])

            return results
        except Exception as e:
            logging.error('Failed to read local image list: ')
            logging.exception(e)
            raise ValueError(e)

    def listRemoteImages(self):
        try:
            remoteImagesLink = Config().get(meta.APP_NAME, '{}.images.remote'.format(meta.APP_NAME.lower()))
            logging.info('Reading remote image list')
            remoteClient = Client(endpoint=remoteImagesLink)
            return remoteImagesList(remoteClient.api.images.aliases.get().json())
        except Exception as e:
            logging.error('Failed to get remote container images: ')
            logging.exception(e)
            raise ValueError(e)

    def listNightlyImages(self):
        try:
            logging.info('Reading nightly remote image list')
            images = requests.get(url='https://vhajdari.github.io/lxd-images/images.json')
            return images.json()['images']
        except Exception as e:
            logging.error('Failed to get remote nightly container images: ')
            logging.exception(e)
            raise ValueError(e)

    def listHubImages(self):
        try:
            logging.info('Listing images')
            result = requests.get('{}/cliListRepos'.format(meta.IMAGE_HUB))

            return result.json()
        except Exception as e:
            logging.error('Failed to list images from kuti.io')
            logging.exception(e)
            raise ValueError(e)

    def detailsRemoteImage(self, alias):
        try:
            remoteImagesLink = Config().get(meta.APP_NAME, '{}.images.remote'.format(meta.APP_NAME.lower()))
            remoteClient = Client(endpoint=remoteImagesLink)
            fingerprint = remoteClient.api.images.aliases[alias].get().json()['metadata']['target']
            return remoteClient.api.images[fingerprint].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def downloadImage(self, image):
        try:
            remoteImagesLink = Config().get(meta.APP_NAME, '{}.images.remote'.format(meta.APP_NAME.lower()))
            logging.info('Downloading remote image:', image)
            remoteClient = Client(endpoint=remoteImagesLink)
            try:
                remoteImage = remoteClient.images.get_by_alias(image)
            except:
                remoteImage = remoteClient.images.get(image)
            newImage = remoteImage.copy(self.client, auto_update=False, public=False, wait=True)
            return self.client.api.images[newImage.fingerprint].get().json()['metadata']
        except Exception as e:
            logging.error('Failed to download image:')
            logging.exception(e)
            raise ValueError(e)

    def deleteImage(self):
        pass

    def listProfiles(self):
        try:
            results = []
            for profile in self.client.api.profiles.get().json()['metadata']:
                results.append(self.client.api.profiles[profile.split('/')[-1]].get().json()['metadata'])

            return results
        except Exception as e:
            raise ValueError(e)

    def listStoragePools(self):
        try:
            results = []
            for profile in self.client.api.storage_pools.get().json()['metadata']:
                results.append(self.client.api.storage_pools[profile.split('/')[-1]].get().json()['metadata'])

            return results
        except Exception as e:
            raise ValueError(e)

    def createProfile(self):
        pass

    def deleteProfile(self):
        pass

    def updateProfile(self):
        pass

    def listNetworks(self):
        try:
            logging.info('Retrieving network list.')
            results = []
            for network in self.client.api.networks.get().json()['metadata']:
                results.append(self.client.api.networks[network.split('/')[-1]].get().json()['metadata'])

            return results
        except Exception as e:
            logging.error('Failed to retrieve network list:')
            logging.exception(e)
            raise ValueError(e)

    def createNetwork(self):
        pass

    def deleteNetwork(self):
        pass

    def updateNetwork(self):
        pass


    def config(self):
        try:
            return self.client.api.get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def hasImage(self, imageInfo):
        lxdModule = LXDModule()
        for image in lxdModule.listLocalImages():
            if image.get('fingerprint') == imageInfo:
                return 'fingerprint'
            for alias in image.get('aliases'):
                if alias.get('name') == imageInfo:
                    return 'alias'
        return None

    def containerExists(self, containerName):
        lxdModule = LXDModule()
        try:
            logging.info('Checking if container exists.')
            container = self.client.containers.get(containerName)
            return True
        except Exception as e:
            logging.error('Failed to verify container:')
            logging.exception(e)
            return False

    def info(self):
        raise NotImplementedError()

    def create(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def restart(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def move(self):
        raise NotImplementedError()

    def clone(self):
        raise NotImplementedError()

    def snapshot(self):
        raise NotImplementedError()