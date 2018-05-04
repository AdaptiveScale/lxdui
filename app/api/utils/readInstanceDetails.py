import platform, sys, os, subprocess
from app.api.models.LXDModule import LXDModule

import logging

def readInstanceDetails():
    instanceDetails = ("Python Version: {}".format(platform.python_version()))
    instanceDetails +=("\nPython Path: {}".format(' '.join(path for path in sys.path)))
    instanceDetails +=("\nLXD Version: {}".format(LXDModule().config()['environment']['server_version']))
    instanceDetails +=("\nLXD Status: {}".format(LXDModule().config()['api_status']))
    instanceDetails +=("\nOS: {}".format(platform.platform()))
    instanceDetails +=("\nLXDUI Path: {}".format(sys.path[0]))
    instanceDetails +=("\nCPU: {}".format(getProcessorDetails()))
    instanceDetails +=("\nMemory: {}MB".format(getMemory()))
    instanceDetails +=("\nDisk: {}".format(getDiskDetails()))
    logging.info(instanceDetails)

def getMemory():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    return int(mem_bytes / (1024. ** 2))

def getProcessorDetails():
    return subprocess.check_output('lscpu', shell=True).strip().decode()

def getDiskDetails():
    return subprocess.check_output('df -h', shell=True).strip().decode()