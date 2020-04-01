from app.api.models.LXDModule import LXDModule
import logging

logging = logging.getLogger(__name__)

class LXCContainer(LXDModule):
    def __init__(self, input):
        self.data = {}
        self.remoteHost = '127.0.0.1'

        if not input.get('name'):
            logging.error('Container name is required for any container operation')
            raise ValueError('Missing container name.')

        self.setName(input.get('name'))
        logging.info('Connecting to LXD')
        super(LXCContainer, self).__init__(remoteHost=self.remoteHost)

        if self.client.containers.exists(self.data.get('name')):
            existing = self.info()
            self.data['config'] = existing['config'];
            self.data['devices'] = existing['devices']

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

        if input.get('imageAlias'):
            self.setImageAlias(input.get('imageAlias'))

        if input.get('autostart') != None:
            self.setBootType(input.get('autostart'))
        else:
            self.setBootType(True)

        if input.get('stateful') != None:
            self.setEphemeral(not input.get('stateful'))
        else:
            self.setEphemeral(False)

        if input.get('newName'):
            self.setNewName(input.get('newName'))

        if input.get('config'):
            self.setConfig(input.get('config'))



    def setImageType(self, input):
        # Detect image type (alias or fingerprint)
        logging.debug('Checking if image {} exists'.format(input))
        tempImageType = self.hasImage(input)

        if not tempImageType:
            logging.error('Image with alias or fingerprint {} not found'.format(input))
            raise ValueError('Image with alias or fingerprint {} not found'.format(input))

        if not self.data.get('source'):
            self.data['source']={'type':'image'}
        self.data['source'][tempImageType] = input


    def setName(self, input):
        logging.debug('Setting image name to {}'.format(input))
        self.data['name'] = input

    def setDescription(self, input):
        logging.debug('Setting image description as {}'.format(input))
        self.data['description'] = input

    def setProfile(self, input):
        logging.debug('Setting image profiles as {}'.format(input))
        self.data['profiles']=input

    def setEphemeral(self, input):
        logging.debug('Setting image ephemeral type to {}'.format(input))
        self.data['ephemeral']=input

    def initConfig(self):
        if not self.data.get('config', None):
            self.data['config']={}

    def setCPU(self, input):
        self.initConfig()
        if input.get('count'):
            logging.debug('Set CPU count to {}'.format(input.get('count')))
            self.data['config']['limits.cpu']=input.get('count')
        if input.get('percentage'):
            if input.get('hardLimitation'):
                self.data['config']['limits.cpu.allowance']='{}ms/100ms'.format(input.get('percentage'))
            else:
                self.data['config']['limits.cpu.allowance'] = '{}%'.format(input.get('percentage'))
            logging.debug('CPU allowance limit set to {}'.format(self.data['config']['limits.cpu.allowance']))

    def setMemory(self, input):
        self.initConfig()
        self.data['config']['limits.memory']='{}MB'.format(input.get('sizeInMB'))
        self.data['config']['limits.memory.enforce'] = 'hard' if input.get('hardLimitation') else 'soft'
        logging.debug('Memory limit set to {} with restrictions set to {}'.format(
            self.data['config']['limits.memory'],
            self.data['config']['limits.memory.enforce']
        ))

    def setNewContainer(self, input):
        self.data['newContainer'] = input

    def setImageAlias(self, input):
        logging.debug('Setting image alias as {}'.format(input))
        self.data['imageAlias'] = input

    def setBootType(self, input):
        self.initConfig()
        self.data['config']['boot.autostart'] = '1' if input else '0'
        logging.debug('Setting autostart boot type to {}'.format(input))

    def setEphemeral(self, input):
        self.initConfig()
        self.data['ephemeral'] = input
        logging.debug('Setting container as ephemeral {}'.format(input))

    def setNewName(self, input):
        self.initConfig()
        logging.debug('Setting new container name as: {}'.format(input))
        self.data['newName'] = input

    def setConfig(self, input):
        logging.debug('Setting key-value for container config')
        self.initConfig()
        for key in input.keys():
            self.data['config'][key] = input[key]

    def info(self):
        try:
            logging.info('Reading container {} information'.format(self.data.get('name')))
            c = self.client.containers.get(self.data.get('name'))

            container = self.client.api.containers[self.data.get('name')].get().json()['metadata']
            container['cpu'] = c.state().cpu
            container['memory'] = c.state().memory
            container['network'] = c.state().network
            container['processes'] = c.state().processes
            container['pid'] = c.state().pid
            container['disk'] = c.state().disk

            return container
        except Exception as e:
            logging.error('Failed to retrieve information for container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def create(self, waitIt=True):
        try:
            logging.info('Creating container {}'.format(self.data.get('name')))
            self.client.containers.create(self.data, wait=waitIt)
            if self.data['config']['boot.autostart'] == '1':
                self.start(waitIt)
            return self.info()
        except Exception as e:
            logging.error('Failed to create container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def delete(self, force=False):
        try:
            logging.info('Deleting container with {} enforcement set to {}'.format(self.data.get('name'), force))
            container = self.client.containers.get(self.data.get('name'))
            if self.info().get('ephemeral'):
                container.stop(wait=True)
                return
            elif force and self.info().get('status') == 'Running':
                container.stop(wait=True)
            container.delete()
        except Exception as e:
            logging.error('Failed to delete container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def update(self):
        try:
            logging.info('Updating container {}'.format(self.data.get('name')))
            container = self.client.containers.get(self.data.get('name'))
            if self.data.get('config'):
                container.config = self.data.get('config')

            if self.data.get('profiles'):
                container.profiles = self.data.get('profiles')

            if self.data.get('description'):
                container.description = self.data.get('description')

            container.save(True)
            if self.data.get('newName'):
                self.rename()
            return self.info()
        except Exception as e:
            logging.error('Failed to update container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def start(self, waitIt=True):
        try:
            logging.info('Starting container {}'.format(self.data.get('name')))
            container = self.client.containers.get(self.data.get('name'))
            container.start(wait=waitIt)
        except Exception as e:
            logging.error('Failed to start container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def stop(self, waitIt=True):
        try:
            logging.info('Stopping container {}'.format(self.data.get('name')))
            container = self.client.containers.get(self.data.get('name'))
            container.stop(wait=waitIt)
        except Exception as e:
            logging.error('Failed to stop container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def restart(self, waitIt=True):
        try:
            logging.info('Restarting container {}'.format(self.data.get('name')))
            container = self.client.containers.get(self.data.get('name'))
            container.restart(wait=waitIt)
        except Exception as e:
            logging.error('Failed to restart container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def move(self):
        pass

    def clone(self):
        try:
            logging.info('Cloning container {}'.format(self.data.get('name')))
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
            logging.error('Failed to clone container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def move(self):
        try:
            logging.info('Moving container {}'.format(self.data.get('name')))
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
            logging.error('Failed to move container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)


    def export(self, force=False):
        try:
            logging.info('Exporting container {}'.format(self.data.get('name')))
            container = self.client.containers.get(self.data.get('name'))
            if force and container.status == 'Running':
                container.stop(wait=True)

            image = container.publish(wait=True)
            image.add_alias(self.data.get('imageAlias'), self.data.get('name'))
            try:
                fingerprint = container.config.get('volatile.base_image')
                self.client.api.images[image.fingerprint].put(json={'properties': self.client.api.images[fingerprint].get().json()['metadata']['properties']})
            except:
                logging.error('Image does not exist.')
            container.start(wait=True)
            return self.client.api.images[image.fingerprint].get().json()['metadata']
        except Exception as e:
            logging.error('Failed to export container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def rename(self, force=True):
        try:
            logging.info('Renaming container {} to {}'.format(self.data.get('name'), self.data.get('newName')))
            if self.data.get('newName'):
                if self.containerExists(self.data.get('newName')):
                    raise ValueError('Container with that name already exists')
            container = self.client.containers.get(self.data.get('name'))
            previousState = container.status
            if previousState == 'Running':
                if force == False:
                    raise ValueError('Container is running')
                container.stop(wait=True)
            container.rename(self.data.get('newName'), True)
            if previousState == 'Running':
                container.start(wait=True)
            self.data['name'] = self.data.get('newName')
            return self.info()
        except Exception as e:
            logging.error('Failed to rename container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)


    def freeze(self, waitIt=True):
        try:
            logging.info('Freezing container {}'.format(self.data.get('name')))
            container = self.client.containers.get(self.data.get('name'))
            container.freeze(wait=waitIt)
        except Exception as e:
            logging.error('Failed to freeze container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)


    def unfreeze(self, waitIt=True):
        try:
            logging.info('Unfreezing container {}'.format(self.data.get('name')))
            container = self.client.containers.get(self.data.get('name'))
            container.unfreeze(wait=waitIt)
        except Exception as e:
            logging.error('Failed to unfreeze container {}'.format(self.data.get('name')))
            logging.exception(e)
            raise ValueError(e)

    def initNetwork(self):
        if not self.data.get('devices', None):
            self.data['devices']={}

    def addNetwork(self, network):
        self.initNetwork()
        self.data['devices'][network['name']]=network
        try:
            container = self.client.containers.get(self.data['name'])
            container.devices = self.data['devices']
            container.save()
            return self.info()
        except Exception as e:
            raise ValueError(e)

    def removeNetwork(self, networkName):
        self.initNetwork()
        del self.data['devices'][networkName]
        try:
            container = self.client.containers.get(self.data['name'])
            container.devices = self.data['devices']
            container.save()
            return self.info()
        except Exception as e:
            raise ValueError(e)

    def addProxy(self, name, proxy):
        self.initNetwork()
        self.data['devices'][name] = proxy
        try:
            container = self.client.containers.get(self.data['name'])
            container.devices = self.data['devices']
            container.save()
            return self.info()
        except Exception as e:
            raise ValueError(e)

    def removeProxy(self, name):
        self.initNetwork()
        del self.data['devices'][name]
        try:
            container = self.client.containers.get(self.data['name'])
            container.devices = self.data['devices']
            container.save()
            return self.info()
        except Exception as e:
            raise ValueError(e)
