from api.src.models.LXDModule import LXDModule

from pylxd import Client


class LXCProfile(LXDModule):

    def __init__(self, input):
        self.client = Client()
        self.input = input

    def info(self):
        try:
            return self.client.api.profiles[self.input.get('name')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def createProfile(self):
        try:
            self.client.profiles.create(self.input.get('name'), config=self.input.get('config'),
                                        devices=self.input.get('devices'))
            return self.info()
        except Exception as e:
            raise ValueError(e)

    def deleteProfile(self):
        try:
            return self.client.api.profiles[self.input.get('name')].delete(json=self.input).json()
        except Exception as e:
            raise ValueError(e)

    def updateProfile(self):
        try:
            self.client.api.profiles[self.input.get('name')].put(json=self.input).json()['metadata']
            return self.info()
        except Exception as e:
            raise ValueError(e)
