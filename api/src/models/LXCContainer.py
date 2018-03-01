from api.src.models.LXDModule import LXDModule

class LXCContainer(LXDModule):
    def __init__(self, input):
        self.data = {}
        self.remoteHost = '127.0.0.1'

        if not input.get('name'):
            raise ValueError('Missing container name.')
        self.setName(input.get('name'))

        if input.get('image'):
            self.setImageType(input.get('image'))

        if input.get('profiles'):
            self.setProfile(input.get('profiles'))

        if input.get('ephemeral'):
            self.setEphemeral(input.get('ephemeral'))

        if input.get('description'):
            self.setDescription(input.get('description'))

        if input.get('cpu'):
            self.setCPU(input.get('cpu'))

        if input.get('memory'):
            self.setMemory(input.get('memory'))

        if input.get('newContainer'):
            self.setNewContainer(input.get('newContainer'))

        super(LXCContainer, self).__init__(remoteHost=self.remoteHost)

    def setImageType(self, input):
        # Detect image type (alias or fingerprint)
        tempImageType = self.hasImage(input)

        if not tempImageType:
            raise ValueError('Image with alias or fingerprint {} not found'.format(input))

        if not self.data.get('source'):
            self.data['source']={'type':'image'}
        self.data['source'][tempImageType] = input


    def setName(self, input):
        self.data['name'] = input

    def setDescription(self, input):
        self.data['description'] = input

    def setProfile(self, input):
        self.data['profiles']=input

    def setEphemeral(self, input):
        self.data['ephemeral']=input

    def initConfig(self):
        if not self.data.get('config', None):
            self.data['config']={}

    def setCPU(self, input):
        self.initConfig()
        if input.get('count'):
            self.data['config']['limits.cpu']=input.get('count')
        if input.get('percentage'):
            if input.get('hardLimitation'):
                self.data['config']['limits.cpu.allowance']='{}ms/100ms'.format(input.get('percentage'))
            else:
                self.data['config']['limits.cpu.allowance'] = '{}%'.format(input.get('percentage'))

    def setMemory(self, input):
        self.initConfig()
        self.data['config']['limits.memory']='{}MB'.format(input.get('sizeInMB'))
        self.data['config']['limits.memory.enforce'] = 'hard' if input.get('hardLimitation') else 'soft'

    def setNewContainer(self, input):
        self.data['newContainer'] = input

    def info(self):
        try:
            return self.client.api.containers[self.data.get('name')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def create(self):
        try:
            self.client.containers.create(self.data, wait=True)
            self.start(waitIt=True)
            return self.info()
        except Exception as e:
            raise ValueError(e)

    def delete(self, force=False):
        try:
            container = self.client.containers.get(self.data.get('name'))
            if force and self.info().get('status') == 'Running':
                container.stop(wait=True)
            container.delete()
        except Exception as e:
            raise ValueError(e)

    def update(self):
        pass

    def start(self, waitIt=True):
        try:
            container = self.client.containers.get(self.data.get('name'))
            container.start(wait=waitIt)
        except Exception as e:
            raise ValueError(e)

    def stop(self, waitIt=True):
        try:
            container = self.client.containers.get(self.data.get('name'))
            container.stop(wait=waitIt)
        except Exception as e:
            raise ValueError(e)

    def restart(self, waitIt=True):
        try:
            container = self.client.containers.get(self.data.get('name'))
            container.restart(wait=waitIt)
        except Exception as e:
            raise ValueError(e)

    def move(self):
        pass

    def clone(self):
        try:
            container = self.client.containers.get(self.data.get('name'))
            if container.status == 'Running':
                container.stop(wait=True)

            copyData = container.generate_migration_data()
            copyData['source'] = {'type': 'copy', 'source': self.data.get('name')}
            copyData['name'] = self.data.get('newContainer')

            newContainer = self.client.containers.create(copyData, wait=True)
            container.start(wait=True)
            newContainer.start(wait=True)
            return self.client.api.containers[self.data.get('newContainer')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)

    def move(self):
        try:
            container = self.client.containers.get(self.data.get('name'))
            if container.status == 'Running':
                container.stop(wait=True)

            copyData = container.generate_migration_data()
            copyData['source'] = {'type': 'copy', 'source': self.data.get('name')}
            copyData['name'] = self.data.get('newContainer')

            newContainer = self.client.containers.create(copyData, wait=True)
            newContainer.start(wait=True)

            container.delete(wait=True)
            return self.client.api.containers[self.data.get('newContainer')].get().json()['metadata']
        except Exception as e:
            raise ValueError(e)