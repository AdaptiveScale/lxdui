from api.src.models.Base import Base

class LXDModule(Base):
    # Default 127.0.0.1 -> Move to Config
    def __init__(self, remoteHost='127.0.0.1'):
        pass

    def listContainers(self):
        pass

    def listLocalImages(self):
        pass

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
