from api.src.models.LXDModule import LXDModule

class LXCImage(LXDModule):
    def __init__(self, input):
        self.data = {}
        if not input.get('remoteHost'):
            self.remoteHost = '127.0.0.1'
        else:
            self.remoteHost = input.get('remoteHost')

        if not input.get('fingerprint'):
            raise ValueError('Missing image fingerprint.')

        self.setFingerprint(input.get('fingerprint'))

        if input.get('image'):
            self.setImage(input.get('image'))


        super(LXCImage, self).__init__(remoteHost=self.remoteHost)


    def setAlias(self, input):
        self.data['alias'] = input

    def setFingerprint(self, input):
        self.data['fingerprint'] = input

    def setImage(self, input):
        self.data['image'] = input

    def getImage(self):
        try:
            return self.client.api.images[self.data.get('fingerprint')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def deleteImage(self):
        try:
            image = self.client.images.get(self.data.get('fingerprint'))
            image.delete()
        except Exception as e:
            raise ValueError(e)