from app.api.models.LXDModule import LXDModule

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

    def info(self, name):
        try:
            return self.client.api.profiles[name].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def createProfile(self):
        try:
            self.client.profiles.create(self.input.get('name'), config=self.input.get('config'),
                                        devices=self.input.get('devices'))

            return self.client.api.profiles[self.input.get('name')].get().json()['metadata']
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
            if self.input.get('new_name'):
                return self.rename()
            return self.info()
        except Exception as e:
            raise ValueError(e)

    def rename(self):
        try:
            profile = self.client.profiles.get(self.input.get('name'))
            profile.rename(self.input.get('new_name'))
            return self.info(self.input.get('new_name'))
        except Exception as e:
            raise ValueError(e)
