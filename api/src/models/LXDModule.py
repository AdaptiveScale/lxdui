from api.src.models.Base import Base

from pylxd import Client

class LXDModule(Base):
    # Default 127.0.0.1 -> Move to Config
    def __init__(self, remoteHost='127.0.0.1'):
        self.client = Client()

    def listContainers(self):
        results = []
        for container in self.client.api.containers.get().json()['metadata']:
            results.append(self.client.api.containers[container.split('/')[-1]].get().json()['metadata'])

        return results

    def listLocalImages(self):
        results = []
        for image in self.client.api.images.get().json()['metadata']:
            results.append(self.client.api.images[image.split('/')[-1]].get().json()['metadata'])

        return results

    def listRemoteImages(self):
        pass

    def downloadImage(self):
        pass

    def deleteImage(self):
        pass

    def listProfiles(self):
        results = []
        for profile in self.client.api.profiles.get().json()['metadata']:
            results.append(self.client.api.profiles[profile.split('/')[-1]].get().json()['metadata'])

        return results

    def createProfile(self):
        pass

    def deleteProfile(self):
        pass

    def updateProfile(self):
        pass

    def listNetworks(self):
        results = []
        for network in self.client.api.networks.get().json()['metadata']:
            results.append(self.client.api.networks[network.split('/')[-1]].get().json()['metadata'])

        return results

    def createNetwork(self):
        pass

    def deleteNetwork(self):
        pass

    def updateNetwork(self):
        pass


    def config(self):
        return self.client.api.get().json()


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