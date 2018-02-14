from api.src.models.Base import Base

from pylxd import Client

class LXDModule():
    # Default 127.0.0.1 -> Move to Config
    def __init__(self, remoteHost='127.0.0.1'):
        self.client = Client()
        self.client.authenticate('')

    def listContainers(self):
        return self.client.containers.all()

    def listLocalImages(self):
        return self.client.images.all()

    def listRemoteImages(self):
        pass

    def downloadImage(self):
        pass

    def deleteImage(self):
        pass

    def listProfiles(self):
        pass

    def createProfile(self):
        pass

    def deleteProfile(self):
        pass

    def updateProfile(self):
        pass

    def listNetworks(self):
        pass

    def createNetwork(self):
        pass

    def deleteNetwork(self):
        pass

    def updateNetwork(self):
        pass