import click
import os
from cli import Config, User, Init, Certificate


APP = "LXDUI"
LXD_URL = 'http://localhost:8443'

'''
Commands:

lui init					                #configures lxdui upon first use - admin password, generate certs
lui start					                #start the app and print the endpoint URL  <http://hostname:port> 
lui stop					                #stop the app
lui restart					                #restart the app
lui status					                #show the pid and the http endpoint for the UI <http://hostname:port> 
lui config show				                #print out running config to console
lui config set lxdui.port <port>		    #set the value for a configuration key
lui cert create				                #generate new SSL certs (overwrite old files)
lui cert list				                #list SSL certs
lui cert delete 				            #remove SSL certs
lui user add -u <username> -p <password>    #create a new user that can access the UI
lui user update -u <username> -p <password> #the user specified in lxdui.admin.user can't be deleted
lui user delete -u <username>			    #remove a user from the auth file
lui user list				                #list the users in the auth file
'''


# click.clear()


def progressBar(iterable):
    c = range(9999)
    with click.progressbar(c, label='exporting...') as bar:
        for i in bar:
            i=None


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
def start():
    """Start LXDUI"""
    click.echo("Starting %s" % APP)


@lui.command()
def stop():
    """Stop LXDUI"""
    click.echo("Stopping %s" % APP)


@lui.command()
def restart():
    """Restart LXDUI"""
    click.echo("Restarting %s" % APP)


@lui.command()
def status():
    """Check the status of LXDUI"""
    click.echo("%s Status" % APP)


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
    User.show()


@user.command()
@click.option('-u', '--username', help='User Name')
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def add(username, password):
    """Create a new user account"""
    User.add(username, password)


@user.command()
@click.option('-u', '--username', nargs=1, help='User Name')
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password')
def update(username, password):
    """Change user password"""
    click.echo("Change user password")
    User.update(username, password)

@user.command()
@click.option('-u', '--username', nargs=1, help='User Name')
def delete(username):
    """Delete a user account"""
    click.echo("Delete user account")
    User.delete(username)


'''
    Config commands
    
    lui config show				                #print out running config to console
    lui config set lxdui.port <port>		    #set the value for a configuration key
'''


@click.group()
def config():
    """List and modify configuration parameters"""
    pass

@config.command()
def show():
    """Show configured parameters"""
    Config.show()

@config.command()
@click.argument('parameter', nargs=1)
@click.argument('value', nargs=1)
def set(parameter, value):
    """Set a configuration parameter"""
    Config.set('LXDUI', parameter, value)



'''
    Commands for certificate management
    
    lui cert create				                #generate new SSL certs (overwrite old files)
    lui cert list				                #list SSL certs
    lui cert delete 				            #remove SSL certs
'''


@click.group()
def cert():
    """List and modify configuration parameters"""
    pass

@cert.command()
@click.option('-p', '--path', nargs=1, help='Path for certificates')
def create(path):
    """Create client certificates"""
    c = Certificate()
    c.save(path + '/test.key', c.key)
    c.save(path + '/test.crt', c.cert)

@cert.command()
def list():
    """Show available certificates"""
    # path = Config().get('LXDUI', 'lxdui.conf.dir')
    key = Config().get('LXDUI', 'lxdui.ssl.key')
    cert = Config().get('LXDUI', 'lxdui.ssl.cert')

    path = 'conf'
    for root, dirs, files in os.walk(path):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext in ['.key', '.crt']:
                click.echo(path + '/' + file)

@cert.command()
def delete():
    """Delete certificates"""
    path = 'conf'
    key = Config().get('LXDUI', 'lxdui.ssl.key')
    cert = Config().get('LXDUI', 'lxdui.ssl.cert')

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
# user.add_command(add)
# user.add_command(update)

if __name__ == '__main__':
    lui()
