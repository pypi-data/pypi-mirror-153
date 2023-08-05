import sys, os, platform
from .ExecThread import *
from .esptool import main as espmain

def esptoolWork(commmand, onLog, onFinish, cdc=None):
    cmd = commmand.split(' ')
    def kprint(*args, **kwargs):
        onLog(args[0])
    try:
        ret = espmain(cmd, kprint, cdc)
        onFinish(0)
    except Exception as e:
        onFinish("ESPTOOL: "+str(e))

def uploadEsp32Firm(port, config, onLog, onFinish, cdc=None):
    if port:
        port = '--port '+port
    
    # esptool.main(commmand)
    cwd = os.getcwd()
    firmPath = os.path.join(cwd, config['firmwarePath'])
    flashAddr = config['flashAddr']

    commmand = '--chip esp32 {} --baud 1024000 write_flash -z --flash_mode dio --flash_freq 40m {} {}'.format(port, flashAddr, firmPath)
    th = threading.Thread(target=esptoolWork, args=(commmand, onLog, onFinish, cdc, ))
    th.daemon = True
    th.start()
    

