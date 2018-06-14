import platform, sys, os, subprocess
import psutil
from app.api.models.LXDModule import LXDModule

import logging

def readInstanceDetails():
    instanceDetails = ("Python Version: {}".format(platform.python_version()))
    instanceDetails +=("\nPython Path: {}".format(' '.join(path for path in sys.path)))
    instanceDetails +=("\nLXD Version: {}".format(getLXDInfo()['environment']['server_version']))
    instanceDetails +=("\nLXD Status: {}".format(getLXDInfo()['api_status']))
    instanceDetails +=("\nOS: {}".format(platform.platform()))
    instanceDetails +=("\nLXDUI Path: {}".format(sys.path[0]))
    instanceDetails +=("\nCPU Count: {}".format(getProcessorDetails()))
    instanceDetails +=("\nMemory: {}MB".format(getMemory()))
    instanceDetails +=("\nDisk used percent: {}".format(getDiskDetails()))
    logging.info(instanceDetails)

def getLXDInfo():
    try:
        info = LXDModule().config()
        return info
    except:
        return {
            'environment': {
                'server_version': 'N/A'
            },
            'api_status': 'N/A'
        }

def getMemory():
    return int(psutil.virtual_memory().total / (1024*1024))

def getProcessorDetails():
    return psutil.cpu_count()

def getDiskDetails():
    return psutil.disk_usage('/').percent