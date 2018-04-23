from app import __metadata__ as meta
from app.lib.conf import Config
from app.lib.auth import User
from app.cli.init import Init
from app.lib.cert import Certificate
from app.api import core
from app.ui.blueprint import uiPages
import click
import os
import time
import subprocess
import logging
log = logging.getLogger(__name__)

APP = meta.APP_NAME

'''
Commands:

lui init					                #configures lxdui upon first use - admin password, generate certs
lui start					                #start the app and print the endpoint URL  <http://hostname:port> 
lui stop					                #stop the app
lui restart					                #restart the app
lui status					                #show the pid and the http endpoint for the UI <http://hostname:port> 
lui config show				                #print out running config to console
lui config set -c <path_to_conf_file>       #use external conf file
lui config set <key> <value>    		    #set the value for a configuration key
lui cert add     				            #add existing certs from file path
lui cert create				                #generate new SSL certs (overwrite old files)
lui cert list				                #list SSL certs
lui cert delete 				            #remove SSL certs
lui user add -u <username> -p <password>    #create a new user that can access the UI
lui user update -u <username> -p <password> #the user specified in lxdui.admin.user can't be deleted
lui user delete -u <username>			    #remove a user from the auth file
lui user list				                #list the users in the auth file
'''


''' Command Groups '''


@click.group()
def lui():
    """LXDUI CLI"""
    pass


''' lui root level group of commands '''


@lui.command()
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def init(password):
    """Initialize and configure LXDUI"""
    click.echo("Initialize and configure %s" % APP)
    Init(password)


@lui.command()
# @click.option('-d', '--daemon', nargs=0, help='Starts the app in the background.')
def start():
    """Start LXDUI"""
    '''
    TODO:  add -d option to start the server as a daemon
    '''
    # if daemon:
    #     #start in the background
    #click.echo("Starting %s" % APP)
    _doStart()


@lui.command()
def stop():
    """Stop LXDUI"""
    _doStop()


@lui.command()
def restart():
    """Restart LXDUI"""


@lui.command()
def status():
    """Check the status of LXDUI"""
    click.echo("%s Status" % APP)


#Private Functions
def _doStart(args=None):
    port = 5000
    try:
        port = int(Config().get('LXDUI', 'lxdui.port'))
    except:
        print('Please initialize {} first.  e.g: {} init '.format(meta.APP_NAME, meta.APP_CLI_CMD))
        exit()

    core.startApp(port, uiPages)

def _doStop(args=None):
    click.echo("Stopping %s" % APP)
    subprocess.Popen("fuser -k {}/tcp".format(Config().get('LXDUI', 'lxdui.port')), shell=True).wait()


@lui.command()
def cwd():
    """Check the status of LXDUI"""
    click.echo(os.getcwd())
    click.echo(os.path.dirname(__file__))
    click.echo(os.path.dirname(os.path.abspath(__file__)))

    # click.echo(os.path.abspath(__file__))
    # click.echo(sys.modules[__name__].__file__)
    # click.echo(os.path.abspath(__file__))
    # click.echo(os.path.realpath(__file__))
    # import inspect
    # click.echo(inspect.getfile(Config()))
    # click.echo(sys.path)
    from configparser import ConfigParser, ExtendedInterpolation
    # c = ConfigParser()
    c = ConfigParser(interpolation=ExtendedInterpolation())
    c.read('/Users/vetoni/PycharmProjects/lxdui/conf/lxdui.conf')
    cd = c.get(APP, 'lxdui.conf.dir')
    a = c.get(APP, 'lxdui.auth.conf')
    click.echo(cd)
    click.echo(a)
    click.echo('{{app_path}}' in a)

''' 
    User level group of commands 

    lui user list				                #list the users in the auth file
    lui user add -u <username> -p <password>    #create a new user that can access the UI
    lui user update -u <username> -p <password> #the user specified in lxdui.admin.user can't be deleted
    lui user delete -u <username>			    #remove a user from the auth file

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

    lui config show				                #print out running config to console
    lui config set <key> <value>		    #set the value for a configuration key
'''


@click.group()
def config():
    """List and modify configuration parameters"""
    pass


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

    lui cert create				                #generate new SSL certs (overwrite old files)
    lui cert list				                #list SSL certs
    lui cert delete 				            #remove SSL certs
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
    c.save(key)
    c.save(crt)


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
lui.add_command(init)
lui.add_command(start)
lui.add_command(stop)
lui.add_command(restart)
lui.add_command(status)
lui.add_command(user)
lui.add_command(config)
lui.add_command(cert)

########################
lui.add_command(init)


if __name__ == '__main__':
    lui()
