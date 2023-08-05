from .ExecThread import *
from .Uf2Manager import *
from .SerialCom import serialList, serialCom
from .uflash import getDisk
from .ImageManager import saveToBmp
from .HardwareHandler import HardwareHandler
from .EspToolMng import uploadEsp32Firm
from .pyboard import Pyboard, PyboardError
from .ampy import Files
from .kerror import KERR
import shutil
import tempfile
from datetime import datetime, timedelta
from functools import wraps
from io import BytesIO
import ast,textwrap
import re

t0=datetime.now()
def throttle(ms):
    throttle_period = timedelta(milliseconds=ms)
    def throttle_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            global t0
            now = datetime.now()
            if now - t0 > throttle_period:
                t0 = now
                return fn(*args, **kwargs)
        return wrapper
    return throttle_decorator

IMGRX = "[^\s]+(\.(?i)(jpg|png|bmp))$"

class MeowbitHandler(HardwareHandler):
  def __init__(self, websocket, extensions, userPath):
    HardwareHandler.__init__(self, websocket, extensions, userPath)
    
  def list_file_pyb(self):
    self.comm.setPybMutex(True)
    # todo: add pyusb support for ampy
    try:
      pyb = Pyboard(self.comm)
      fp = Files(pyb)
      allFiles = fp.ls()
      self.sendResp(self.pid, {'files': allFiles})
    except (Exception,PyboardError) as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.LIST_FILE_FAIL})
    finally:
      self.comm.setPybMutex(False)

  def list_file(self):
    if self.ext['pyb'] or 'pyb' in self.params:
      return self.list_file_pyb()
    os.path.getsize
    dest = getDisk(self.ext['thumbdisk'],"2M")
    if dest:
        fileFilter = None
        if 'filter' in self.params:
            fileFilter = self.params['filter']
        files = os.listdir(dest)
        allFiles = []
        for f in files:
            fileExtension = os.path.splitext(f)[1]
            if fileFilter:
                if fileExtension in fileFilter:
                    allFiles.append(f)
            else:
                allFiles.append(f)
        self.sendResp(self.pid, {'files': allFiles})
    else:
        self.sendResp(self.pid, None, {"error": "cannot find disk", "code": KERR.LIST_FILE_FAIL})

  def disk_info_pyb(self):
    self.comm.setPybMutex(True)
    # todo: add pyusb support for ampy
    try:
      pyb = Pyboard(self.comm)
      fp = Files(pyb)
      info = fp.fsinfo()
      self.sendResp(self.pid, info)
    except (Exception,PyboardError) as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.GET_DISK_INFO_FAIL})
    finally:
      self.comm.setPybMutex(False)

  def disk_info(self):
    if self.ext['pyb'] or 'pyb' in self.params:
      return self.disk_info_pyb()
    dest = getDisk(self.ext['thumbdisk'],"2M")
    if dest:
        total, used, free = shutil.disk_usage(dest)
        self.sendResp(self.pid, {'total': total, 'used': used, 'free': free})

  def upload_file_pyb(self, params):
    try:
      content = base64.b64decode(params['content'])
      fileName = params['fileName']
      self.comm.setPybMutex(True)
      # todo: add pyusb support for ampy
      pyb = Pyboard(self.comm)
      fp = Files(pyb)
      fp.put(fileName, content)
      self.sendResp(self.pid, {'status': 'ok', 'file': fileName})
    except (Exception,PyboardError) as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.UPLOAD_IMAGE_FAIL, 'file': fileName})
    finally:
      self.comm.setPybMutex(False)

  def upload_file(self):
    if self.ext['pyb'] or 'pyb' in self.params:
      return self.upload_file_pyb(self.params)

    dest = getDisk(self.ext['thumbdisk'],"2M")
    if not dest:
        self.sendResp(self.pid, None, {"error": 'no_device', "code": KERR.CANNOT_FIND_DISK})
        return
    fileName = self.params['fileName']
    destPath = os.path.join(dest, fileName)
    total, used, free = shutil.disk_usage(dest)
    if free < 100*1024:
        self.sendResp(self.pid, None, {"error": "not enough space", "code": 103, 'file': destPath})
        return
    try:
        with open(destPath, 'wb') as output:
            # logger.info("copy %s to %s" %(fileName, destPath))
            content = base64.b64decode(self.params['content'])
            output.write(content)
            output.flush()
            os.fsync(output) # fix for windows flush with a quantity delay
            self.sendResp(self.pid, {'status': 'ok', 'file': destPath})
    except Exception as e:
        # self.sendResp(self.pid, None, {"error": str(e), "code": 103, 'file': destPath})
        self.sendResp(self.pid, None, {"error": str(e), "code": KERR.UPLOAD_IMAGE_FAIL, 'file': destPath})

  def upload_image_pyb(self, params):
    base64Input = True if 'base64' in params and params['base64'] else False
    fmt = params['fmt'] if 'fmt' in params else 'png'
    fileName = params['fileName']
    if fileName.find('.') > 0:
      fileName = fileName[0:fileName.find('.')]
    width = None
    if 'width' in params:
      width = int(params['width'])
    try:
      imageIo = BytesIO()
      saveToBmp(params['content'], imageIo, width, fmt=fmt, base64Input=base64Input)

      self.comm.setPybMutex(True)
      # todo: add pyusb support for ampy
      pyb = Pyboard(self.comm)
      fp = Files(pyb)
      savePath = fileName+'.'+fmt

      @throttle(100)
      def cb(num, total):
          self.sendReq("upload-status", {"text": "[%s] %s/%s" %(savePath, num, total)})
      fp.put(savePath, imageIo.getvalue(), cb)
      self.sendResp(self.pid, {'status': 'ok', 'file': fileName})
    except (Exception,PyboardError) as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.UPLOAD_IMAGE_FAIL, 'file': savePath})
    finally:
      self.sendReq("upload-status", {})
      self.comm.setPybMutex(False)


  def upload_image(self):
    if self.ext['pyb'] or 'pyb' in self.params:
      return self.upload_image_pyb(self.params)
    dest = getDisk(self.ext['thumbdisk'],"2M")
    fileName = self.params['fileName']
    if not dest:
      self.sendResp(self.pid, None, {"error": 'no_device', "code": KERR.CANNOT_FIND_DISK})
      return
    destPath = os.path.join(dest, fileName)
    total, used, free = shutil.disk_usage(dest)
    if free < 100*1024:
      self.sendResp(self.pid, None, {"error": "not enough space", "code": 103, 'file': destPath})
      return
    try:
      width = None
      if 'width' in self.params:
          width = int(self.params['width'])
      destPath = os.path.splitext(destPath)[0]+'.bmp'
      saveToBmp(self.params['content'], destPath, width)
      self.sendResp(self.pid, {'status': 'ok', 'file': destPath})
    except Exception as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.UPLOAD_IMAGE_FAIL, 'file': destPath})
  

  def delete_file_pyb(self, params):
    try:
      fileName = params['fileName']
      # todo: add pyusb support for ampy
      self.comm.setPybMutex(True)
      pyb = Pyboard(self.comm)
      fp = Files(pyb)
      fp.rm(fileName)
      self.sendResp(self.pid, {'status': 'ok'})
    except (Exception,PyboardError) as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.UPLOAD_IMAGE_FAIL, 'file': fileName})
    finally:
      self.comm.setPybMutex(False)

  def delete_file(self):
    if self.ext['pyb'] or 'pyb' in self.params:
      return self.delete_file_pyb(self.params)
    dest = getDisk(self.ext['thumbdisk'],"2M")
    ret = -1
    if dest:
      fileName = self.params['fileName']
      filePath = os.path.join(dest, fileName)
      if os.path.exists(filePath):
        print(filePath)
        os.remove(filePath)
        ret = 0
    self.sendReq("extension-method", {"extensionId": self.ext['id'], "func": "onDelDone", "msg": ret})   

  def contrastFile(self,boardfile,filedict):
    boardfile_hash = {}
    filedict_hash = {}
    for file_name in boardfile:
      boardfile_hash[boardfile[file_name]["hash"]] = file_name
    for file_name in filedict:
      filedict_hash[filedict[file_name]["hash"]] = file_name

    fileToCopy = list(set(filedict_hash).difference(boardfile_hash))
    fileToDelete = list(set(boardfile_hash).difference(filedict_hash))
    sameFile = list(set(filedict_hash).intersection(boardfile_hash))

    return fileToCopy,sameFile,fileToDelete,boardfile_hash,filedict_hash

  def sync_files(self):
    if self.ext['pyb'] or 'pyb' in self.params:
      return self.sync_files_pyb(self.params)
    try:
      skipList = ['main.py',
                  'VERSION',
                  'filedict.json',
                  'wifi_cfg.py',
                  'boot.py',
                  'pybcdc.inf',
                  'README.txt',
                  'System Volume Information',
                  '.fseventsd']
      dest = getDisk(self.ext['thumbdisk'],"2M")
      # 传入的json
      filedict = self.params['filedict']
      files = os.listdir(dest)
      # needUpdate = False
      # 掌机内的json
      boardfile = {}
      import platform
      if platform.system() == "Windows":
        try:
          cmdStat = os.system('Chkdsk /f {0}'.format(dest))  # 防止因文件损坏导致的问题
        
        # print('fix hard',cmdStat)
          if cmdStat == 1:  # 需要修复返回代码1，正常返回代码0
            time.sleep(0.5)
        except:
          pass

      if os.path.isfile(os.path.join(dest, 'filedict.json')):
        try:
          fp = open(os.path.join(dest, 'filedict.json'))
          boardfile = json.load(fp)
        except Exception as erro:
          import traceback
          traceback.print_exc()
          for bdfile in files:
            if bdfile not in skipList:
              filePath = os.path.join(dest, bdfile)
              try:
                os.remove(filePath)
              except:
                import traceback
                traceback.print_exc()
        finally:
          fp.close()
          os.remove(os.path.join(dest, 'filedict.json'))
      else:
        for bdfile in files:
          if bdfile not in skipList:
            filePath = os.path.join(dest, bdfile)
            try:
              os.remove(filePath)
            except:
              import traceback
              traceback.print_exc()
      realRootFile = os.listdir(os.path.join(dest))
      fileToCopy,sameFile,fileToDelete,boardfile_hash,filedict_hash = self.contrastFile(boardfile,filedict)

      # 删除掌机上不在资源包中的文件
      for deleteHash in fileToDelete:
        fileName = boardfile_hash[deleteHash]
        if (fileName in skipList) or fileName.startswith('.'):
          continue
        if re.search(IMGRX, fileName):
          fileName = os.path.splitext(fileName)[0]+'.bmp'
        if fileName in realRootFile:
          fpath = os.path.join(dest, fileName)
          os.remove(fpath)
          self.sendReq("upload-status", {"text": "delete file: %s" %(fileName)})
          # needUpdate = True
      # copy files to target
      for copyHash in fileToCopy:
        
        fname = filedict_hash[copyHash]
        f = filedict[fname]
        if 'content' in f:
          content = f['content']
          del filedict[fname]['content']
        elif 'base64' in f:
          content = base64.b64decode(f['base64'])
          del filedict[fname]['base64']
        elif 'url' in f:
          r = requests.get(f['url'], verify=False)
          del filedict[fname]['url']
          if r.ok:
            content = r.content
          else:
            raise RuntimeError("download %s failed" %url)
          # todo: support url download format
        if re.search(IMGRX, fname):
          fielIo = BytesIO(content)
          imageIo = BytesIO()
          saveToBmp(fielIo, imageIo, fmt='bmp')
          content = imageIo.getvalue()
          filedict[fname]['saved'] = len(content)
          fname = os.path.splitext(fname)[0]+'.bmp'
        # todo: support image write
        # todo: stm32 use direct file copy
        with open(os.path.join(dest, fname), 'wb') as fp:
          fp.write(content)
          self.sendReq("upload-status", {"text": "%s >> %s" %(fname, dest)})
          os.fsync(fp)
        # needUpdate = True

      for sameHash in sameFile:
        fname = filedict_hash[sameHash]
        try:
          del filedict[fname]['base64']
        except:
          del filedict[fname]['url']
      # if needUpdate:
      with open(os.path.join(dest, 'filedict.json'), 'w') as fp:
        json.dump(filedict, fp, indent=4)
        os.fsync(fp)
      self.sendResp(self.pid, {'status': 'ok'})
    except (Exception,PyboardError) as e:
      import traceback
      tb_err = traceback.format_exc()
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.SYNC_FILE_FAIL, "traceback": tb_err})
    finally:
      self.sendReq("upload-status", {})
      self.comm.setPybMutex(False)

  def sync_files_pyb(self, params):
    try:
      filedict = self.params['filedict']
      self.comm.setPybMutex(True)
      pyb = Pyboard(self.comm)
      # needUpdate = False
      fp = Files(pyb)
      files = fp.ls()
      # realfiles = []
      skipList = ['VERSION',
                  'main.py',
                  'filedict.json',
                  'wifi_cfg.py']
      realRootFile = []
      for realFile in files:
        realRootFile.append(realFile.split(' - ')[0][1:])
      # print(realRootFile)
      try:
        filetxt = fp.get('filedict.json')
        fp.rm('filedict.json')
      except RuntimeError as err:
        for pybfile in realRootFile:
          if pybfile not in skipList:
            fp.rm(pybfile)
        # print(str(err))
        filetxt = '{}'
      try:
        boardfile = json.loads(filetxt)
      except Exception as err:
        boardfile = {}
        import traceback
        traceback.print_exc()
        for pybfile in realRootFile:
          if pybfile not in skipList:
            fp.rm(pybfile)
      fileToCopy,sameFile,fileToDelete,boardfile_hash,filedict_hash = self.contrastFile(boardfile,filedict)
      # 删除掌机上不在资源包中的文件
      for deleteHash in fileToDelete:
        fileName = boardfile_hash[deleteHash]
        if fileName in skipList:
          continue
        if re.search(IMGRX, fileName):
          fileName = os.path.splitext(fileName)[0]+'.png'
        if fileName in realRootFile:
          fp.rm(fileName)
          self.sendReq("upload-status", {"text": "delete file: %s" %(fileName)})
        # needUpdate = True

      for copyHash in fileToCopy:
        fname = filedict_hash[copyHash]
        f = filedict[fname]
        if 'content' in f:
          content = f['content']
          del filedict[fname]['content']
        elif 'base64' in f:
          content = base64.b64decode(f['base64'])
          del filedict[fname]['base64']
        elif 'url' in f:
          r = requests.get(f['url'], verify=False)
          if r.ok:
            content = r.content
            del filedict[fname]['url']
          else:
            raise RuntimeError("download %s failed" %url)
            # todo: support url download format
        if re.search(IMGRX, fname):
          fielIo = BytesIO(content)
          imageIo = BytesIO()
          saveToBmp(fielIo, imageIo, fmt='png')
          content = imageIo.getvalue()
          filedict[fname]['saved'] = len(content)
          fname = os.path.splitext(fname)[0]+'.png'
        @throttle(100)
        def cb(num, total):
          self.sendReq("upload-status", {"text": "[%s] %s/%s" %(fname, num, total)})
        # todo: support image write
        # todo: stm32 use direct file copy
        fp.put(fname, content, cb)

        # needUpdate = True

      for sameHash in sameFile:
        fname = filedict_hash[sameHash]
        try:
          del filedict[fname]['base64']
        except:
          del filedict[fname]['url']


      # if needUpdate:
      fp.put('filedict.json', json.dumps(filedict))

      self.sendResp(self.pid, {'status': 'ok'})
    except (Exception,RuntimeError,PyboardError) as e:
      import traceback
      tb_err = traceback.format_exc()
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.SYNC_FILE_FAIL, "traceback": tb_err})
    finally:
      self.sendReq("upload-status", {})
      self.comm.setPybMutex(False)

  def normal_repl(self):
    try:
      self.comm.setPybMutex(True)
      pyb = Pyboard(self.comm)
      pyb.enter_normal_repl()
      self.sendResp(self.pid, {'status': 'ok'})
    except (Exception,PyboardError) as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.GO_NORMAL_REPL_FAIL})
    finally:
      self.comm.setPybMutex(False)

  def uname_info(self):
    try:
      self.comm.setPybMutex(True)
      pyb = Pyboard(self.comm)
      fp = Files(pyb)
      info = fp.uname()
      self.sendResp(self.pid, {'info': info})
    except (Exception,PyboardError) as e:
      self.sendResp(self.pid, None, {"error": str(e), "code": KERR.GO_NORMAL_REPL_FAIL})
    finally:
      self.comm.setPybMutex(False)

  def upload_firmware(self):
    if self.ext["fwtype"] == "uf2":
        # check if in bootloader
        # dest = getDisk(self.ext['thumbdisk'],"2M")
        dest = getDisk(self.ext['thumbdisk'])

        if dest:
          for i in range(5):
            try:
              self.comm.write(b'import machine\r\nmachine.bootloader()\r\n')
            except:
              pass
            time.sleep(2)
            dest_boot = getDisk('ARCADE-F4')
            if dest_boot:
              break      #  进入bootload成功，执行后面的步骤
          if not dest_boot:
            self.sendResp(self.pid, None, {"error": 'enter bootloader faid', "code": KERR.UPLOAD_FIRM_FAIL})
        def onDone(msg, err):
            if err:
                self.sendResp(self.pid, None, {"error": msg, "code": KERR.UPLOAD_FIRM_FAIL})
            else:
                self.sendResp(self.pid, {'status': 'ok', 'msg': msg})
        uploadUf2(self.ext, self.params, self.sendReq, self.userPath, onDone)
    elif self.ext["fwtype"] == "esptool" or self.ext["fwtype"] == "esp":
        port=None
        # todo: add pyusb firmware retore
        if self.comm:
            tmp = tempfile.mkdtemp()
            if 'url' in self.params:
                url = self.params['url']
                self.sendReq("upload-status", {"text": "Downloading %s" %url})
                r = requests.get(url, verify=False)
                if r.ok:
                  firmPath = os.path.join(tmp, os.path.basename(url))
                  with open(firmPath, 'wb') as f:
                      f.write(r.content)
                else:
                  self.sendResp(self.pid, None, {"error": "Firmware download fail", "code": KERR.UPLOAD_FIRM_FAIL})
                  return
            self.sendReq('connclose')
            def onLog(msg):
                # print('>>>', msg)
                msg = re.findall(r'[(](.*?)[%]', msg)
                if len(msg) == 0:
                  msg = [0]
                
                self.sendReq("upload-status", {"text": "#", "progress": int(msg[0])})
            def onDone(err):
                self.comm.setPybMutex(False)
                self.sendReq("upload-status", {})
                if err:
                    self.sendResp(self.pid, None, {"error": str(err), "code": KERR.UPLOAD_FIRM_FAIL})
                else:
                    shutil.rmtree(tmp)
                    self.sendResp(self.pid, {'status':'ok'})
            config = {
                'firmwarePath': firmPath,
                'flashAddr': self.ext['flashAddr'] if 'flashAddr' in self.ext else 0x1000
            }
            if self.comm.ser:
              port=self.comm.ser.name
              self.comm.close()
              uploadEsp32Firm(port, config, onLog, onDone)
            elif self.comm.dev: # filter driver mode
              self.comm.setPybMutex(True)
              uploadEsp32Firm("USB_CDC", config, onLog, onDone, self.comm)
        else:
          self.sendResp(self.pid, None, {"error": "no download port", "code": KERR.UPLOAD_FIRM_FAIL})