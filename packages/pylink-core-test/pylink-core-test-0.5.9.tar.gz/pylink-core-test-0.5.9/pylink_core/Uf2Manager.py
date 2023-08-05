import subprocess, signal, platform
import sys, os, time
import json
import logging
import threading
import locale
import shutil
import base64, re, requests
from io import BytesIO
from .kerror import KERR
from .ExecThread import *
from .uflash import copyHex, flash, getDisk

logger = logging.getLogger(__name__)


def uploadFirmTask(firmPath, ext, sendReq, onDone):
    def uploadProgress(p, total, prompt="#"):
        progress = int(p/total*100)
        sendReq("upload-status", {"text": prompt, "progress": progress})
    if firmPath.startswith("http"):
        firmPath = requests.get(firmPath).content
    try:
        

        (code, ret) = copyHex(firmPath, callback=uploadProgress)
        
        print("upload return %s %s" %(code, ret))
        newVol = None
        sendReq("upload-status")
        if code != 0:
            print('code != 0 error')
            onDone(ret, 1)
        else:
            # wait new thumbdisk show up
            if 'thumbdisk' in ext:
                DISKNAME = ext['thumbdisk']
                while not newVol:
                    newVol = getDisk(DISKNAME)
                    time.sleep(0.5)
            onDone(newVol,0)
    except Exception as err:
        print('exception error')
        onDone(str(err), 1)

def uploadUf2(ext, params, sendReq, userPath, onDone):

    sendReq("upload-status", {"text": "Initializing Upload", "progress": "1"})
    if "code" in params:
        if "boardName" in params:
            firmware = ext["board"][params["boardName"]]["runtime"]
            firmPath = os.path.join(ext['fullpath'], firmware)
        else:
            firmPath = os.path.join(ext['fullpath'], ext['runtime'])
        logger.info("upload %s" %firmPath)
        pycode = bytes(params['code'], encoding = "utf8")
        (code, ret) = flash(path_to_runtime=firmPath, python_script=pycode)
        sendReq("upload-status")
    else:
        if "base64" in params:
            firmPath = params['base64']
        elif "url" in params:
            firmPath = params['url']
        else:
            firmPath = os.path.join(ext['fullpath'], ext['firmware'])
        th = threading.Thread(target=uploadFirmTask,args=(firmPath, ext, sendReq, onDone))
        th.start()
        
    