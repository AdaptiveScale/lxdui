from api.src.models.LXDModule import LXDModule

from pylxd import Client
from pylxd.exceptions import LXDAPIException


class LXCProfile(LXDModule):

    def __init__(self, input):
        self.client = Client()
        self.input = input
        if not self.input.get('name'):
            raise ValueError('Missing profile name.')
        # if not self.input.get('config'):
        #    raise ValueError('Missing config.')
        # if not self.input.get('devices'):
        #    raise ValueError('Missing devices.')

    def info(self):
        try:
            return self.client.api.profiles[self.input.get('name')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def createProfile(self):
        try:
            self.client.profiles.create(self.input.get('name'), config=self.input.get('config'),
                                        devices=self.input.get('devices'))
        except Exception as e:
            raise ValueError(e)
        return self.info()

    def deleteProfile(self):
        try:
            return self.client.api.profiles[self.input.get('name')].delete(json=self.input).json()
        except LXDAPIException as e:
            raise ValueError(e.response.json()['error'])

    def updateProfile(self):
        try:
            self.client.api.profiles[self.input.get('name')].put(json=self.input).json()['metadata']
        except Exception as e:
            raise ValueError(e)
        return self.info()
