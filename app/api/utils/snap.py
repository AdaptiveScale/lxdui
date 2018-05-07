import os
from pathlib import Path, PurePath
from app import __metadata__ as meta
APP = meta.APP_NAME.lower()
'''
In this component the app needs to figure out in what environment it is running in.
This will determine where logs and config files will be stored.
If the app was installed using setuptools then in all likelihood the app has access to
the user's HOME directory.

If the app was installed as a snap then the paths will be confined to the snap environment.
Paths will be remapped and controlled by snapd.

Snap Environment Variables:
SNAP - Directory where the snap is mounted
SNAP_COMMON - Directory for system data that is common across revisions of a snap
SNAP_USER_DATA - Directory for user data, backed up and restored across snap refresh and snap revert operations.


#check is HOME directory is writable - this path will be different in a snap
#check if there is an existing config in ~/.config/lxdui
#if it exists than use that
#on init prompt user to overwrite the ~/.config/lxdui directory

store logs in SNAP_COMMON
store conf in SNAP_USER_DATA
'''

def writable(path):
    return os.access(path, os.W_OK)

def genConf(path):
    if Path(path).exists():
        files = Path.glob('*.conf')
        if ['auth.conf', 'log.conf', APP + '.conf'] in files:
            return False
    else:
        return True

home = str(Path.home())
snap_conf = os.getenv('SNAP_USER_DATA')

if snap_conf:
    if writable(snap_conf):
        #create directory for config data
        Path.mkdir(meta.APP_NAME.lower())
    else:
        #the app is not a snap so create the config dir under the user's home
        app_conf_dir = Path.joinpath(Path.home(), '.config/{}'.format(APP))
        #if there's a preexisting configuration then skip it otherwise create the dir
        if not genConf(app_conf_dir):
            print('A previous config exists. app_conf_dir = {}'.format(app_conf_dir))
        else:
            print('{} does not exist'.format(app_conf_dir))
            print('creating config directory for {}'.format(APP))
            #if the app is running as a Snap then user the SNAP_COMMON directory
            snap_log = os.getenv('SNAP_COMMON')
            if  snap_log:
                Path.mkdir(Path(snap_log).joinpath('.config/lxdui'), parents=True)

