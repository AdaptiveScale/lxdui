from app.api.models.Base import Base
from app.api.utils.remoteImageMapper import remoteImagesList

from pylxd import Client
import requests


class LXDModule(Base):
    # Default 127.0.0.1 -> Move to Config
    def __init__(self, remoteHost='127.0.0.1'):
        self.client = Client()

    def listContainers(self):
        try:
            results = []
            for container in self.client.api.containers.get().json()['metadata']:
                results.append(self.client.api.containers[container.split('/')[-1]].get().json()['metadata'])

            return results
        except Exception as e:
            raise ValueError(e)

    def listLocalImages(self):
        try:
            results = []
            for image in self.client.api.images.get().json()['metadata']:
                results.append(self.client.api.images[image.split('/')[-1]].get().json()['metadata'])

            return results
        except Exception as e:
            raise ValueError(e)

    def listRemoteImages(self):
        try:
            #remoteClient = Client(endpoint='https://images.linuxcontainers.org')
            #return remoteClient.api.images.get().json()['metadata']

            images = requests.get(url='https://us.images.linuxcontainers.org/1.0/images/aliases')
            return remoteImagesList(images.json())
        except Exception as e:
            raise ValueError(e)

    def detailsRemoteImage(self, alias):
        try:
            response = requests.get(url='https://us.images.linuxcontainers.org/1.0/images/aliases/{}'.format(alias))
            image_details = requests.get(url='https://us.images.linuxcontainers.org/1.0/images/{}'.format(response.json()['metadata']['target']))
            return image_details.json()
        except Exception as e:
            raise ValueError(e)

    def downloadImage(self, image):
        try:
            #response = requests.get(url='https://us.images.linuxcontainers.org/1.0/images/aliases/{}'.format(self.data.get('image')))
            #image_details = requests.get(url='https://us.images.linuxcontainers.org/1.0/images/{}'.format(response.json()['metadata']['target']))

            remoteClient = Client(endpoint='https://images.linuxcontainers.org')
            remoteImage = remoteClient.images.get_by_alias(image)
            newImage = remoteImage.copy(self.client, auto_update=False, public=False, wait=True)

            return self.client.api.images[newImage.fingerprint].get().json()['metadata']
        except Exception as e:
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

    def createProfile(self):
        pass

    def deleteProfile(self):
        pass

    def updateProfile(self):
        pass

    def listNetworks(self):
        try:
            results = []
            for network in self.client.api.networks.get().json()['metadata']:
                results.append(self.client.api.networks[network.split('/')[-1]].get().json()['metadata'])

            return results
        except Exception as e:
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