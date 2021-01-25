from app import __metadata__ as meta
from app.lib.conf import Config
from app.lib.auth import User
from app.cli.init import Init
from app.lib.cert import Certificate
from app.api import core
from app.ui.blueprint import uiPages
from app.api.models.LXCImage import LXCImage
import click
import os
import signal
import time
import subprocess
import logging
log = logging.getLogger(__name__)

APP = meta.APP_NAME

'''
Commands:

lxdui init					                #configures lxdui upon first use - admin password, generate certs
lxdui start					                #start the app and print the endpoint URL  <http://hostname:port> 
lxdui stop					                #stop the app
lxdui restart					                #restart the app
lxdui status					                #show the pid and the http endpoint for the UI <http://hostname:port> 
lxdui config show				                #print out running config to console
lxdui config set -c <path_to_conf_file>       #use external conf file
lxdui config set <key> <value>    		    #set the value for a configuration key
lxdui cert add     				            #add existing certs from file path
lxdui cert create				                #generate new SSL certs (overwrite old files)
lxdui cert list				                #list SSL certs
lxdui cert delete 				            #remove SSL certs
lxdui user add -u <username> -p <password>    #create a new user that can access the UI
lxdui user update -u <username> -p <password> #the user specified in lxdui.admin.user can't be deleted
lxdui user delete -u <username>			    #remove a user from the auth file
lxdui user list				                #list the users in the auth file
'''


''' Command Groups '''



@click.group()
@click.version_option(version=meta.VERSION, message='{} v{} \n{}\n{}'.format(meta.APP_NAME, meta.VERSION, meta.AUTHOR, meta.AUTHOR_URL))
# @click.version_option(message=meta.APP_NAME + ' version ' + meta.VERSION + '\n' + meta.AUTHOR + '\n' + meta.AUTHOR_URL )
def lxdui():
    """LXDUI CLI"""
    pass

''' lxdui root level group of commands '''
@lxdui.command()
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def init(password):
    """Initialize and configure LXDUI"""
    click.echo("Initialize and configure %s" % APP)
    Init(password)


@lxdui.command()
# @click.otion('-b', '--daemon', default=False, help='Run in background as a daemon.')
# @click.otion('-c', '--conf', default=False, help='Config file.')
# @click.otion('-p', '--port', default=False, help='TCP Port number.')
@click.option('-d', '--debug', default=False, help='Run the app in debug mode')
def start(debug):
    """Start LXDUI"""

    click.echo('{} ver. {} -- (c){}'.format(meta.APP_NAME, meta.VERSION, meta.AUTHOR))
    click.echo(meta.AUTHOR_URL)

    # Private Functions
    def _start(debug=False):
        host = '0.0.0.0'
        port = 5000
        try:
            host = Config().get('LXDUI', 'lxdui.host')
            port = int(Config().get('LXDUI', 'lxdui.port'))
        except:
            print('Please initialize {} first.  e.g: {} init '.format(meta.APP_NAME, meta.APP_CLI_CMD))
            exit()

        core.start(host, port, debug, uiPages)

    if debug:
        _start(debug=True)
    else:
        _start()


@lxdui.command()
def stop():
    """Stop LXDUI"""
    click.echo("Stopping %s" % APP)
    core.stop()


@lxdui.command()
def restart():
    """Restart LXDUI"""
    host = Config().get('LXDUI', 'lxdui.host')
    port = int(Config().get('LXDUI', 'lxdui.port'))
    click.echo('Restarting with defaults.')
    core.stop()
    click.echo('Port = {} \nDebug = False\nMode = Foreground\n'.format(port))
    time.sleep(3)
    core.start(host, port, False, uiPages)

@lxdui.command()
def status():
    """Check the status of LXDUI"""
    click.echo("{} Status:".format(APP))

    s = core.status()
    if s == 'STOPPED':
        click.echo('STOPPED')
    else:
        click.echo("=============")
        for k, v in s.items():
            click.echo(' {} : {}'.format(k, v))


@click.group()
def image():
    """Work with image registry"""
    pass

@image.command()
@click.argument('fingerprint', nargs=1)
def prep(fingerprint):
    """Prepare an image for upload"""
    try:
        input = {}
        image = LXCImage({'fingerprint': fingerprint})

        # Export Image - Image registry
        path = image.exportImage(input)

        click.echo("Image prepared successfully.")
        click.echo("The image path is: {}".format(path))
        click.echo("Modify the image.yaml, upload the logo and update README.md")
        click.echo("To publish the image use the command:")
        click.echo("lxdui image push -u <uid> -p <pwd> <image_fingerprint>")
    except Exception as e:
        click.echo("LXDUI failed to prepare the image.")
        click.echo(e.__str__())

@image.command()
@click.argument('fingerprint', nargs=1)
@click.option('-u', '--username', nargs=1, help='Username')
@click.option('-p', '--password', nargs=1, help='Password')
def push(fingerprint, username, password):
    """Push an image to hub.kuti.io"""
    try:
        input = {}
        input['username'] = username
        input['password'] = password

        image = LXCImage({'fingerprint': fingerprint})

        # Export Image - Image registry
        image.pushImage(input)

        click.echo("Image pushed successfully.")
    except Exception as e:
        click.echo("LXDUI failed to push the image.")
        click.echo(e.__str__())

@image.command()
@click.argument('fingerprint', nargs=1)
def pull(fingerprint):
    """Pull an image from hub.kuti.io"""
    try:
        input = {}

        image = LXCImage({'fingerprint': fingerprint})

        print("Downlaoding image with fingerprint {}".format(fingerprint))
        # Import Image - Image registry
        image.importImage(input)

        click.echo("Image imported successfully.")
    except Exception as e:
        click.echo("LXDUI failed to download/import the image.")
        click.echo(e.__str__())

@image.command()
def list():
    """List images from hub.kuti.io"""
    try:
        input = {}
        image = LXCImage({'fingerprint': 'a'})

        # List Images from kuti.io
        print (image.listHub(input))

    except Exception as e:
        click.echo("LXDUI failed to list the images from kuti.io.")
        click.echo(e.__str__())

''' 
    User level group of commands 

    lxdui user list				                #list the users in the auth file
    lxdui user add -u <username> -p <password>    #create a new user that can access the UI
    lxdui user update -u <username> -p <password> #the user specified in lxdui.admin.user can't be deleted
    lxdui user delete -u <username>			    #remove a user from the auth file

'''


# @click.group(chain=True)
@click.group()
def user():
    """Work with user accounts"""
    pass


@user.command()
def list():
    """Show all configured user accounts"""
    click.echo("User Accounts:")
    User().show()


@user.command()
@click.option('-u', '--username', help='User Name')
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def add(username, password):
    """Create a new user account"""
    User().add(username, password)


@user.command()
@click.option('-u', '--username', nargs=1, help='User Name')
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def update(username, password):
    """Change user password"""
    click.echo("Change user password")
    User().update(username, password)


@user.command()
@click.option('-u', '--username', nargs=1, help='User Name')
def delete(username):
    """Delete a user account"""
    click.echo("Delete user account")
    User().delete(username)


'''
    Config commands

    lxdui config show				                #print out running config to console
    lxdui config set <key> <value>		    #set the value for a configuration key
'''


@click.group()
def config():
    """List and modify configuration parameters"""
    pass

@config.command()
def env():
    """Show environment variables"""
    click.echo('HOME = '.format(os.getenv('HOME')))
    click.echo('LXDUI_LOG = '.format(os.getenv('LXDUI_LOG')))
    click.echo('LXDUI_CONF = '.format(os.getenv('LXDUI_CONF')))
    click.echo('SNAP = '.format(os.getenv('SNAP')))
    click.echo('SNAP_NAME = '.format(os.getenv('SNAP_NAME')))
    click.echo('SNAP_VERSION = '.format(os.getenv('SNAP_VERSION')))
    click.echo('SNAP_REVISION = '.format(os.getenv('SNAP_REVISION')))
    click.echo('SNAP_ARCH = '.format(os.getenv('SNAP_ARCH')))
    click.echo('SNAP_USER_DATA = '.format(os.getenv('SNAP_USER_DATA')))
    click.echo('SNAP_USER_COMMON = '.format(os.getenv('SNAP_USER_COMMON')))
    click.echo('SNAP_DATA = '.format(os.getenv('SNAP_DATA')))
    click.echo('SNAP_COMMON = '.format(os.getenv('SNAP_COMMON')))
    click.echo('SNAP_LIBRARY_PATH = '.format(os.getenv('SNAP_LIBRARY_PATH')))



@config.command()
def show():
    """Show configured parameters"""
    Config().show()


@config.command()
@click.argument('parameter', nargs=1)
@click.argument('value', nargs=1)
def set(parameter, value):
    """Set a configuration parameter"""
    Config().set(APP, parameter, value)


'''
    Commands for certificate management

    lxdui cert create				                #generate new SSL certs (overwrite old files)
    lxdui cert list				                #list SSL certs
    lxdui cert delete 				            #remove SSL certs
'''


@click.group()
def cert():
    """Work with certificates"""
    pass


@cert.command()
@click.option('-c', '--cert', nargs=1, help='Path to the certificate file')
@click.option('-k', '--key', nargs=1, help='Path to the key file')
def add(cert, key):
    """Add preexisting certificates"""
    if (os.path.exists(key) and os.path.exists(cert)) and (os.path.isfile(key) and os.path.isfile(cert)):
        conf = Config()
        conf.set(APP, '{}.ssl.key'.format(APP.lower()), key)
        conf.set(APP, '{}.ssl.cert'.format(APP.lower()), cert)
        conf.save()
    else:
        log.info("Error reading user provided key and certificate. key={} cert={} ".format(key, cert))
        raise Exception("Please check your paths and try again")


@cert.command()
def create():
    """Create client certificates"""
    c = Certificate()
    key, crt = c.create()
    c.save(APP.lower(),key)
    c.save(APP.lower(),crt)


@cert.command()
def list():
    """Show available certificates"""
    # path = Config().get('LXDUI', 'lxdui.conf.dir')
    key = Config().get(APP, '{}.ssl.key'.format(APP.lower()))
    cert = Config().get(APP, '{}.ssl.cert'.format(APP.lower()))

    path = 'conf'
    for root, dirs, files in os.walk(path):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext in ['.key', '.crt']:
                click.echo(os.path.join(path, file))


@cert.command()
def delete():
    """Delete certificates"""
    path = 'conf'
    key = Config().get(APP, '{}.ssl.key'.format(APP.lower()))
    cert = Config().get(APP, '{}.ssl.cert'.format(APP.lower()))

    try:
        os.remove(key)
        os.remove(cert)
    except IOError as e:
        click.echo(e)


# Add commands
lxdui.add_command(init)
lxdui.add_command(start)
lxdui.add_command(stop)
lxdui.add_command(restart)
lxdui.add_command(status)
lxdui.add_command(user)
lxdui.add_command(config)
lxdui.add_command(cert)
lxdui.add_command(image)


if __name__ == '__main__':
    lxdui()
