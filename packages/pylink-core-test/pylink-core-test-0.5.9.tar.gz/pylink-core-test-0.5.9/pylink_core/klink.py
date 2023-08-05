# -*- coding:utf-8 -*-
import sys, os
import json
import time
import threading
import struct
import base64
import shutil
import platform
from flask import request

from .ExecThread import *
from .MessageHandler import handle
from .Uf2Manager import *
from .SerialCom import serialList, serialCom
from .uflash import getDisk
from .ImageManager import saveToBmp

extensions = {
    'meowbit': {
        "id": "meowbit",
        "fullpath": os.getcwd(),
        "name": "Meowbit",
        "name_zh": "喵比特",
        "version": "1.0.0",
        "type": "micropy",
        "fwtype": "uf2",
        "replmode": True,
        "execmode": True,
        "firmware": "firmware.uf2",
        "thumbdisk": "PYBFLASH",
        "pyb": False
    }, 
    'meow32': {
        "id": "meow32",
        "fullpath": os.getcwd(),
        "name": "Meow32",
        "name_zh": "喵先生",
        "version": "1.0.0",
        "type": "micropy",
        "fwtype": "esptool",
        "replmode": True,
        "execmode": True,
        "pyb": True
    }
}
userPath = None
pioPath = None
server = None
uihandler = None
cloudVar = {}
cloudClients = {}

# def enumExtensionDir(args):
#     global userPath
#     userPath = args.user
#     if not userPath:
#         userPath = os.getcwd()
#     print("User Path: %s" %userPath)

def echo_socket(ws):
    print("New socket %s" %ws)
    handle(ws, extensions, userPath)

# @app.route('/test/<case>/<path:filename>')
# def loadTestCase(case, filename):
#     return send_from_directory(os.path.join(os.getcwd(), 'test', case), filename)

def installdriver():
    if platform.system() == "Windows" and platform.release() == '7':
        # infPath = os.path.join(userPath, "pybcdc.inf")
        # if platform.machine().endswith('64'):
        #     n = os.system('%%SystemRoot%%\\Sysnative\\pnputil.exe -i -a %s' %(infPath))
        # else:
        #     n = os.system('pnputil.exe -i -a %s' %(infPath))
        return str(0)
    else:
        return "只有windows7用户才需要装驱动哦～"

# @app.route('/readdisk/<prompt>/<path:filename>')
# def readdisk(prompt, filename):
#     try:
#         n = getDisk(prompt)
#         a = open(os.path.join(n, filename),"r").read()
#         return a
#     except Exception as err:
#         return '',403

def waitdisk(prompt, retry=1):
    sz = request.args.get('size')
    timeoutCnt = int(retry)
    while timeoutCnt > 0:
        timeoutCnt-=1
        n = getDisk(prompt, sz)
        if n:
            return n
        if timeoutCnt > 0:
            time.sleep(1)
    return "Cannot find disk", 403

def run(app, sockets):
    print('klink run')
    global userPath
    if not userPath:
        userPath = os.getcwd()
    sockets.add_url_rule('/hardware', 'echo_socket', echo_socket)
    app.add_url_rule('/hardware/installdriver', 'installdriver', installdriver)
    app.add_url_rule('/hardware/waitdisk/<prompt>/<retry>', 'waitdisk', waitdisk)
    
