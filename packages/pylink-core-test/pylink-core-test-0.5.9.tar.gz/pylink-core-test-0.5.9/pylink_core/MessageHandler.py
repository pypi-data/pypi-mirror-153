from .HardwareHandlerFactory import HardwareHandlerFactory
from .ExecThread import *
from .Uf2Manager import *
from .SerialCom import serialList, serialCom
from .uflash import getDisk
from .ImageManager import saveToBmp
from .kerror import KERR
import threading
import time
ws = None
h = None
flag = True
clientId = 0
def getWsStatus():
    global ws
    global h
    global flag
    global clientId
    while flag:
        if ws.closed:
            h.disconnect()
            flag = False
            clientId += 1
            h.addClientId()
        time.sleep(0.01)

def handle(websocket, extensions, userPath):
    global ws
    global h
    global flag
    global clientId
    ws = websocket
    clientId = 0
    flag = True
    thread_flag = threading.Thread(target=getWsStatus)
    thread_flag.start()
    hardwareHandlerFactory = HardwareHandlerFactory()
    h = hardwareHandlerFactory.handle('meowbit', websocket, extensions, userPath)
    while not ws.closed and flag:
        message = ws.receive()
        if not message:
            continue
        try:
            h.handle(message, clientId)
        except Exception as err:
            print("WS err %s" %err)
            h.sendReq('ws-error', {'code': KERR.WEBSOCKET_ERR, 'msg': str(err)})
            continue
    print("WS connection closed")
    flag = False
    h.disconnect()
    
  