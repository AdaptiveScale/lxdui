# -*- coding: utf-8 -*-
# Copyright © 2017 AdaptiveScale, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

#VERSION
from app_metadata import __version__ as LXDUI_VERSION, __giturl__ as LXDUI_GITURL

from flask import Flask, render_template, request, redirect, url_for, Response, flash, session
from pylxd import Client
from helpers.response import Response
import json
import uuid
import os
from subprocess import Popen
#arguments
import argparse
#update remote images
import requests
from bs4 import BeautifulSoup
from timeit import default_timer as timer
import time


#Bridge Network Configuration
from helpers.BridgeNetwork import BridgeNetwork
#lxc version
import subprocess
#FLASK-LOGIN
import flask_login
from helpers.login_manage import login_manager
from helpers.login_manage import User

app = Flask(__name__)

#can be dynamically generated each time ...
#app.secret_key = str(uuid.uuid4()).replace('-','')
app.secret_key = 's3cr3tk3y1'
print "="*32
print "APP_SECRET_KEY = {}".format(app.secret_key)

app.config['TEMPLATES_AUTO_RELOAD'] = True

my_path = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(my_path, "conf/config.json")
remote_images_file = os.path.join(my_path, "conf/data.json")
#DEFAULT
app.config['LXDUI_USERNAME'] = "admin"
app.config['LXDUI_PASSWORD'] = "admin"
app.config['LXDUI_PORT'] = 5000

#LOGIN MANAGER - FLASK login_manage
login_manager.init_app(app)

with open(config_file, 'r') as f:
    credentials = json.load(f)
    app.config['LXDUI_USERNAME'] = credentials['username']
    app.config['LXDUI_PASSWORD'] = credentials['password']

def connect():
    try:
        conn = Client()
        conn.authenticate('123123aa')
        return { "error" : False, "conn" : conn}
    except Exception, e:
        return { "error" : True, "message" : "We have trouble connecting to the LXD daemon. LXC/LXD might not be installed or either daemon not initialised up properly !"}

def list_of_local_images():
    client = connect()
    if client['error']:
        return { "error" : True, "message" : "We have trouble connecting to the LXD daemon. LXC/LXD might not be installed or either daemon not initialised up properly !"}
    client = client['conn']
    #======================

    images = client.images.all()
    imagesArr = []
    num = 0
    for img in images:
        if (img.aliases != []):
            num += 1
            imagesArr.append({'aliases': img.aliases[0], 'properties': img.properties, 'size': img.size, 'fingerprint': img.fingerprint})
            
    return { "error" : False, 'list' : imagesArr, "count" : num }

#==================
# CONTEXT PROCESSOR
#==================
@app.context_processor
def pass_lxdui_version():
    return { "lxdui_current_version" : LXDUI_VERSION, "lxdui_git_url" : LXDUI_GITURL}

@app.context_processor
def get_lxc_version():
    try:
        p = subprocess.Popen(["lxc" , "--version"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        output_rez,err_rez = p.communicate()
    except Exception,e:
        return { "LXC_installed" : False }
    ver = float((output_rez).strip())
    color = "warning"
    
    b = ver - int(ver)
    minor_ver = int(str(b)[2:])
    if int(ver) >= 2 and minor_ver >= 3 :
        color = "success"
    return { "LXC_installed" : True, "LXC_version" :  ver, "LXC_label_color" : color}
#==================
# CONTEXT PROCESSOR
#==================

@app.route('/test')
def test():
    client = connect()
    if client['error']:
        response = Response({'success': False, 'payload': client['message']})
        return response.success()
    client = client['conn']

    try:
        container = client.containers.get("cnt-1")

        MAC_ADDR = 'N/A'
        PID = 'N/A'
        PROCESSES = 'N/A'
        NETWORK = 'N/A'
        RAM_MEM = 'N/A'
        CPU_USG = 'N/A'
        
        if container.status == "Running":
            PID = container.state().pid
            PROCESSES = container.state().processes
            NETWORK = container.state().network
            RAM_MEM = container.state().memory
            CPU_USG = container.state().cpu
            #rectify lo
            if NETWORK.has_key('lo'):
                del NETWORK['lo']
        
        MAC_HWADDR_KEY = "volatile.eth0.hwaddr"
        for key in container.expanded_config.keys():
            if "hwaddr" == key[-6:]:
                MAC_HWADDR_KEY =  key
        if MAC_HWADDR_KEY in container.expanded_config.keys():
            MAC_ADDR = str(container.expanded_config[MAC_HWADDR_KEY]).upper()
        

        IMAGE_OS = None
        if "image.distribution" in container.expanded_config.keys():
            IMAGE_OS = str(container.expanded_config["image.distribution"]).capitalize()
        else:
            IMAGE_OS = str(container.expanded_config["image.os"]).capitalize()
        
        OS_METADATA = {"name" : IMAGE_OS,
                        "release" : str(container.expanded_config["image.release"]).capitalize(),
                        "architecture" : str(container.expanded_config["image.architecture"])}

        if container.expanded_config.has_key("image.version"):
            OS_METADATA.update({"version" : str(container.expanded_config["version"])})
        
        CONTAINER_RESOURCE_CONSTRAINS = []
        for ex_c_k in container.expanded_config.keys():
            if ex_c_k[:6] == 'limits':
                CONTAINER_RESOURCE_CONSTRAINS.append({ str(ex_c_k[7:]) : str(container.expanded_config[ex_c_k]) })

        rez = { 'name': container.name,
                    'memory' : RAM_MEM,
                    'cpu_usage' : CPU_USG,
                    'OS' : OS_METADATA,
                    'architecture': container.architecture,
                    'created_at': container.created_at,
                    'status': str(container.status).upper(),
                    'profiles': container.profiles,
                    'MAC_addr': MAC_ADDR,
                    'pid': PID,
                    'process_count': PROCESSES,
                    'network_interfaces': NETWORK,
                    'resource_constrains' : CONTAINER_RESOURCE_CONSTRAINS}

        response = Response({"error" : False, "result" : rez})
        return response.success()

    except Exception, e:
        return str({"error": True, "error_message": str(e).upper() })

@app.route('/')
def home():
    if session.has_key('user_id'):
        if session['user_id'] == app.config['LXDUI_USERNAME']:
            return redirect(url_for("containers"))
            
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_usr = str(request.form['username'].strip())
        form_pass = str(request.form['password'].strip())
        if form_usr == app.config['LXDUI_USERNAME'] and form_pass == app.config['LXDUI_PASSWORD']:
            #SUCCESS
            user = User()
            user.id = app.config['LXDUI_USERNAME']
            flask_login.login_user(user)
            #SUCCESS
            flash('Successfully logged in !','success')
            return redirect(url_for("containers"))
        else:
            #TRY-AGAIN
            flash('Username or Password are incorrect !','error')
            return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route("/logout", methods=['GET'])
def logout():
    flash('Successfully logged out !','info')
    flask_login.logout_user()
    return redirect(url_for("home"))




@app.route('/containers')
@flask_login.login_required
def containers():
    return render_template("containers.html", auto_refresh = request.args.has_key("auto_refresh"), currentpage = "containers")

@app.route('/containers-list', methods=['POST'])
@flask_login.login_required
def containers_list():
    client = connect()
    if client['error']:
        response = Response({'success': False, 'payload': client['message']})
        return response.success()
    client = client['conn']
    #======================

    response = []
    containers = client.containers.all()
    for container in containers:
        IP_ADDR = "N/A"
        if container.status.lower() == "running":
            try:
                net_key = [key for key in container.state().network.keys() if key != 'lo'][0]#Exclude the LOOPBACK
                IP_ADDR = str(container.state().network[net_key]['addresses'][0]['address'])
            except:
                pass
        #OS-metadata

        if "image.distribution" in container.expanded_config.keys():
            IMAGE_OS = str(container.expanded_config["image.distribution"]).capitalize()
        else:
            IMAGE_OS = str(container.expanded_config["image.os"]).capitalize()
        
        if "image.release" in container.expanded_config.keys():
            IMAGE_REL = container.expanded_config["image.release"].capitalize()
        else:
            IMAGE_REL = str(container.expanded_config["image.version"])

        OS_METADATA = {"name" : IMAGE_OS,
                        "release" : IMAGE_REL,
                        "architecture" : str(container.expanded_config["image.architecture"])}


        response.append({'name': container.name,
            'ipaddress': IP_ADDR,
            'status': container.status,
            'created_at': container.created_at,
            'OS' : OS_METADATA
            })

    data = {'success': True, 'payload': response}
    response = Response(data)
    return response.success()

@app.route('/images')
@flask_login.login_required
def images():
    with open(remote_images_file, 'r') as f:
        remote_images_count = len(json.load(f))
    
    rez = list_of_local_images()
    if rez["error"] is True:
        return render_template("images_NO_LXC.html",  currentpage = "images")

    data = {"current_local_image_number" : rez['count'], "current_cached_remote_images" : remote_images_count, 'image_list' : rez['list']}
    return render_template("images.html", data = data, currentpage = "images")

@app.route('/check-image', methods=['POST'])
@flask_login.login_required
def check_cached_image():
    img_alias = request.form['img_alias']
    #------------------------------------
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================

    try:
        target_img = client.images.get_by_alias(img_alias)
        data = {'success': True, 'image_exists' : True }
        response = Response(data)
        return response.success()
    except Exception, e:
        data = {'success': True, 'image_exists' : False }
        response = Response(data)
        return response.success()
    
@app.route('/stop', methods=['POST'])
@flask_login.login_required
def stop_container():
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================
    containerName = request.form['containerName']
    container = client.containers.get(containerName)
    container.stop(wait = True)
    data = {'success': True, 'message': 'Container ' +containerName+ ' successfully stopped !', 'container_name' : containerName}
    response = Response(data)
    return response.success()

@app.route('/start', methods=['POST'])
@flask_login.login_required
def start_container():
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================
    
    containerName = request.form['containerName']
    container = client.containers.get(containerName)
    
    try:
        container.start(wait = True)
    except Exception, e:
         response = Response({'success': False, 'message':' Container <{}> : '.format(containerName) + str(e) })
         return response.success()


    IP_ADDR = "N/A"
    try:
        net_key = [key for key in container.state().network.keys() if key != 'lo'][0]#Exclude the LOOPBACK
        IP_ADDR = str(container.state().network[net_key]['addresses'][0]['address'])
    except:
        pass

    data = {'success': True, 
            'message':'Container ' +containerName+ ' successfully started',
            'container_name' : containerName,
            'ip' : IP_ADDR }
    response = Response(data)
    return response.success()

@app.route('/restart', methods=['POST'])
@flask_login.login_required
def restart():
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================
    containerName = request.form['containerName']
    container = client.containers.get(containerName)

    container.restart(wait = True)
    data = {'success': True, 'message': 'Container ' +containerName+ ' successfully restarted' , 'container_name' : containerName}
    response = Response(data)
    return response.success()



#=====================
# NETWORK ============
#=====================
@app.route('/network', methods=['GET'])
@flask_login.login_required
def network_get():
    bridge_net = BridgeNetwork()
    main_config = bridge_net.get_lxd_main_bridge_config()

    if main_config['error']:
        return render_template("network_nolxdbr0.html", error_message = main_config['message'],  currentpage = "network")
    #return str(main_config['result'])
    return render_template("network.html", network = main_config['result'],  currentpage = "network")

@app.route('/network', methods=['POST'])
@flask_login.login_required
def network_post():
    bridge_net = BridgeNetwork()

    result = bridge_net.validate_form(request.form)
    
    if result['error']:
        flash( result['message'] ,'error')
    else:
        lxc_terminal_tasks = bridge_net._form_to_LXC_SET_TASK(result['validated_data'])
        executed = bridge_net._execute_LXC_NETWORK_TERMINAL( lxc_terminal_tasks )
        flash( str(executed['spitout']) ,'success')
        #restart all containers
        main_config = bridge_net.get_lxd_main_bridge_config()
        if main_config.has_key('used_by'):
            if len(main_config['used_by']) > 0:
                #======================
                client = connect()
                if client['error']:
                    response = Response(client)
                    return response.bad_request()
                client = client['conn']
                #======================
                for cnt_name in main_config['used_by']:
                    container = client.containers.get(cnt_name)
                    print ">> Restarting container <{}> !".format(cnt_name)
                    container.restart()

    return redirect(url_for('network_get'))
    
#=====================
# NETWORK ============
#=====================

@app.route('/delete', methods=['POST'])
@flask_login.login_required
def delete_container():
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================

    container = None
    try:
        containerName = request.form['containerName']
        container = client.containers.get(containerName)
    except Exception, e:
        data = {'success': False, 'payload': 'There is no such container by name <{}> !'.format(containerName)}
        response = Response(data)
        return response.bad_request()
    
    if container.status.lower() == 'running':
        container.stop(wait = True)

    container.delete(wait=True)
    data = {'success': True, 'message': 'Container <{}> has been successfully deleted !'.format(containerName), "container_name" : containerName }
    response = Response(data)
    return response.success()

@app.route('/create-container/<desc>/<fingerprint>/<selected>/<host>', methods=['GET'])
@flask_login.login_required
def create_container(desc=None, fingerprint=None, selected = None, host = None):
    return render_template('createcontainer.html', description=desc, fingerprint=fingerprint, selected=selected, host=host)


@app.route('/launch-container', methods=['POST'])
@flask_login.login_required
def launch_container():
    #=============
    img_alias = request.form['img_alias']
    containerName = request.form['containerName']
    #=============
    config = {'name': containerName,
              'ephemeral': False,#'config': {'limits.cpu': '2', 'limits.memory': '1GB'},
              'source': {'type': 'image',
                         'alias': img_alias }
             }
    #=============

    
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================

    #pre-check container name
    if client.containers.exists(containerName):
        data = {'success': False,
                'payload': "Container with name <{0}> can not be created because it already exists !".format( containerName ),
                'move_next' : True }
        response = Response(data)
        return response.success()
    

    local_cached_OS = None
    try:
        local_cached_OS = client.images.get_by_alias( img_alias )
    except Exception, e:
        if str(e).lower() == "not found" :
            #>>START download it locally
            try:
                linux_repo = Client(endpoint='https://images.linuxcontainers.org')
            except Exception, e:
                print str(e)
                #NO INTERNET
                data = {'success': False,
                        'payload': "NO INTERNET CONNECTION to download the LXC Image <{}> !".format( img_alias ),
                        'move_next' : False }
                response = Response(data)
                return response.success()

            try:
                selected_image = linux_repo.images.get_by_alias( img_alias )
            except Exception, e:
                data = {'success': False,
                        'payload': "There is no LXC IMAGE from the LXC Linux official repo, identified by this alias <{0}> !".format( img_alias ),
                        'move_next' : False }
                response = Response(data)
                return response.success()

            new_local_image = selected_image.copy(client, auto_update=False, public=False, wait=True)
            new_local_image.add_alias( img_alias, str(selected_image.properties["description"]))
            local_cached_OS = new_local_image
            #<<END download it locally
    
    #move on creating from LOCAL OS cached image
    new_container = client.containers.create( config, wait=True)
    try:
        new_container.start(wait = True)
    except Exception, e:
         response = Response({'success': False, 'payload':' Container <{}> : '.format(containerName) + str(e), 'move_next' : True})
         return response.success()

    data = {'success': True,
             'payload': "Container <{0}> has been successfully launched from image <{1}> !".format( containerName ,img_alias),
             'container_name' : containerName,
             'move_next' : True}
    response = Response(data)
    return response.success()      
    

@app.route('/remote-images', methods=['GET'])
@flask_login.login_required
def remote_images():
    with open(remote_images_file, 'r') as f:
        data = json.load(f)

    imagesArr = []
    for img in data:
        imagesArr.append(img)
    rdata = {'success': True, 'payload': imagesArr}
    response = Response(rdata)
    return response.success()


@app.route('/local-images', methods=['GET'])
@flask_login.login_required
def local_images():
    rez = list_of_local_images()
    if rez['error']:
        response = Response(rez)
        return response.bad_request()

    data = {'success': True, 'payload': rez['list']}
    response = Response(data)
    return response.success()

@app.route('/delete-image', methods=['POST'])
@flask_login.login_required
def delete_local_image():
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================
    img_alias = request.form['image_alias']
    try:
        local_image = client.images.get_by_alias(img_alias)
        local_image.delete(wait = True)

        data = {'success': True, 'payload': 'Image with alias <{}> has been successfully deleted !'.format(img_alias) , 'img_alias' : img_alias}
        response = Response(data)
        return response.success()
    except:
        data = {'success': False, 'payload': 'Image with alias <{}> has not found !'.format(img_alias)}
        response = Response(data)
        return response.bad_request()


def retrieve_image_size(alias_term):
    #https://us.images.linuxcontainers.org/1.0/images/aliases/alpine/3.3/amd64/default
    url_request_img = 'https://us.images.linuxcontainers.org/1.0/images/aliases/{0}'.format(alias_term)
    print url_request_img
    r = requests.get(url_request_img)
    image_fingerprint_target = r.json()["metadata"]["target"]

    r1 = requests.get('https://us.images.linuxcontainers.org/1.0/images/'+image_fingerprint_target)
    return {"size" : r1.json()["metadata"]["size"],
            "filename" : str(r1.json()["metadata"]["filename"]) ,
            "description" : str(r1.json()["metadata"]["properties"]["description"]) }


@app.route('/update-remote-images', methods=['GET'])
@flask_login.login_required
def update_remote_images():
    #==============
    start = timer()
    #==============
    r = requests.get('https://uk.images.linuxcontainers.org/')
    soup = BeautifulSoup(r.text)
    all_trs = soup.find('table', {'class': 'table table-striped'}).findAll('tr')[1:]

    imagesArr = []
    for tr in all_trs:
        tds = tr.findAll('td')
        #-----
        temp = { "distr" : str(tds[0].text), "release" : str(tds[1].text), "arch" : str(tds[2].text), "build_ts" : str(tds[4].text) }
        img_alias_term = "{}/{}/{}/default".format(tds[0].text, tds[1].text, tds[2].text)
        tmp_d = retrieve_image_size(img_alias_term)
        temp.update(tmp_d)
        #-----        
        imagesArr.append( { "size" : temp["size"],
                    "properties": {
                        "release": temp["release"],
                        "build": temp["build_ts"],
                        "distribution": temp["distr"],
                        "architecture": temp["arch"],
                        "description":  temp["description"]
                    },
                    "aliases": {
                        "description": temp["description"],
                        "name": img_alias_term ,
                        "target": img_alias_term
                    }} )

    #==============
    end = timer()
    #==============

    with open(remote_images_file, 'w') as f:
        json.dump(imagesArr, f)
    
    data = {'success': True, 'payload': "Linux official remote list has been cached in <data.json> and it only took {} sec !".format(round(end - start, 4)) }
    response = Response(data)
    return response.success()

@app.route('/container-ip/<container_name>', methods=['GET'])
@flask_login.login_required
def container_ip(container_name):
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================
    try:
        container = client.containers.get(container_name)
        data = { 'error' : False, "container_name" : container_name }

        loop_times = 8

        while( (container.status == 'Running') and (loop_times > 0) ):
            arr_of_dicts = container.state().network.get('eth0')['addresses']

            for item in arr_of_dicts:
                if item['family'].lower() == 'inet':
                    data['IP'] = item['address']
                    #break
                    response = Response(data)
                    return response.success()
            
            loop_times -= 1
            time.sleep(0.3)
        
        #out of the loop
        data['IP'] = "N/A"

        response = Response(data)
        return response.success()

    except Exception, e:
        data = { "error": True,  "container_name" : container_name , "message": str(e).upper() }
        response = Response(data)
        return response.success()


@app.route('/container/<container_name>', methods=['GET'])
@flask_login.login_required
def container_details(container_name=None):
    client = connect()
    if client['error']:
        response = Response(client)
        return response.bad_request()
    client = client['conn']
    #======================
    try:
        container = client.containers.get(container_name)

        MAC_ADDR = 'N/A'
        PID = 'N/A'
        PROCESSES = 'N/A'
        NETWORK = 'N/A'
        RAM_MEM = 'N/A'
        CPU_USG = 'N/A'
        
        if container.status == "Running":
            PID = container.state().pid
            PROCESSES = container.state().processes
            NETWORK = container.state().network
            RAM_MEM = container.state().memory
            CPU_USG = container.state().cpu
            #rectify lo
            if NETWORK.has_key('lo'):
                del NETWORK['lo']
        
        MAC_HWADDR_KEY = "volatile.eth0.hwaddr"
        for key in container.expanded_config.keys():
            if "hwaddr" == key[-6:]:
                MAC_HWADDR_KEY =  key
        if MAC_HWADDR_KEY in container.expanded_config.keys():
            MAC_ADDR = str(container.expanded_config[MAC_HWADDR_KEY]).upper()
        

        IMAGE_OS = None
        if "image.distribution" in container.expanded_config.keys():
            IMAGE_OS = str(container.expanded_config["image.distribution"]).capitalize()
        else:
            IMAGE_OS = str(container.expanded_config["image.os"]).capitalize()
        
        if "image.release" in container.expanded_config.keys():
            IMAGE_REL = container.expanded_config["image.release"].capitalize()
        else:
            IMAGE_REL = str(container.expanded_config["image.version"])

        OS_METADATA = {"name" : IMAGE_OS,
                        "release" : IMAGE_REL,
                        "architecture" : str(container.expanded_config["image.architecture"])}

        
        CONTAINER_RESOURCE_CONSTRAINS = []
        for ex_c_k in container.expanded_config.keys():
            if ex_c_k[:6] == 'limits':
                CONTAINER_RESOURCE_CONSTRAINS.append({ str(ex_c_k[7:]) : str(container.expanded_config[ex_c_k]) })

        rez = { 'name': container.name,
                    'memory' : RAM_MEM,
                    'cpu_usage' : CPU_USG,
                    'OS' : OS_METADATA,
                    'architecture': container.architecture,
                    'created_at': container.created_at,
                    'status': str(container.status).upper(),
                    'profiles': container.profiles,
                    'MAC_addr': MAC_ADDR,
                    'pid': PID,
                    'process_count': PROCESSES,
                    'network_interfaces': NETWORK,
                    'resource_constrains' : CONTAINER_RESOURCE_CONSTRAINS}

        data_rez = {"error" : False, "result" : rez}
        return render_template('container-details.html', auto_refresh = request.args.has_key("auto_refresh"), data_rez = data_rez, currentpage = "container / "+container_name )
       
    except Exception, e:
        data_rez = {"error": True, "message": str(e).upper(), "c_name" : container_name}
        return render_template('container-details.html', data_rez = data_rez, currentpage = "container / "+container_name)

#-------------------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser(description='lxdui v{0}'.format(LXDUI_VERSION))

    parser.add_argument(
            '-p', '--port',
            action='store',
            type=int,
            dest='port',
            default=5000,
            metavar='<PORT_NUMBER>',
            help='port to listen on. <PORT_NUMBER> defaults to <5000>'
    )

    parser.add_argument('-d', '--debug',
                        dest='debug',
                        action='store_true', 
                        help='<DEBUG> feature by default is <OFF>. Can be enabled via <-d> or <--debug>')
    parser.add_argument('-l', '--local',
                        dest='local', action='store_true',
                        help='The application by default starts on <0.0.0.0>. To modify <lxd-ui> to start locally just pass <-l> or <--local>' )
    
    parser.add_argument(
            '-c', '--credentials',
            action='store',
            type=str,
            dest='credentials',
            default="{0}:{1}".format(credentials["username"], credentials["password"]),
            metavar='<USERNAME:PASSWORD>',
            help='The credentials to be used for authentication !'
    )


    args = parser.parse_args()
    debug_txt = "ON" if args.debug else "OFF"
    server_target = "127.0.0.1" if args.local else "0.0.0.0"

    #password manipulation
    temp = args.credentials.split(":")
    app.config['LXDUI_USERNAME'] = temp[0]
    app.config['LXDUI_PASSWORD'] = temp[1]
    #password manipulation
    app.config['LXDUI_PORT'] = args.port
    
    print "="*32
    print "Starting lxdui v{1} on port {0}".format(app.config['LXDUI_PORT'], LXDUI_VERSION)
    print "-"*32
    print "DEBUG feature: {}".format(debug_txt)
    print "-"*32
    print "Credentials: {0}:{1}> !".format(app.config['LXDUI_USERNAME'], app.config['LXDUI_PASSWORD'])
    print "="*32

    app.run(host = server_target, port = args.port, debug = args.debug, threaded = True)

if __name__ == '__main__':
    main()
