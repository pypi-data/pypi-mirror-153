# -*- coding:utf-8 -*-

import subprocess, signal, platform
import os
import threading
import locale

class ExecThread(threading.Thread):
    def __init__(self, cmd, cwd, outputCb, onFinish, extraEnv={}):
        self.running = True
        self.cmdList = []
        if type(cmd) == list:
            self.cmdList = cmd
        else:
            self.cmdList = [cmd]
        self.cwd = cwd
        self.env = {**os.environ, **extraEnv}
        self.onFinish = onFinish
        self.outputCb = outputCb
        threading.Thread.__init__(self)

    def run(self):
        try:
            while len(self.cmdList) > 0 and self.running:
                cmd = self.cmdList.pop(0)
                if platform.system() == "Windows":
                    self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.cwd, shell=True, env=self.env)
                else:
                    self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.cwd,
                                                    shell=True, preexec_fn=os.setsid, env=self.env)

                while self.process.poll() is None:
                    line = self.process.stdout.readline()
                    if self.outputCb:
                        self.outputCb(line)
                    # else:
                    #     print('>>', ret)
                # print('exec done',self.process.poll())
            if self.onFinish:
                self.onFinish(self.process.poll())
        except Exception as e:
            if self.onFinish:
                self.onFinish(e)

    def killTh(self):
        if self.process.returncode == None:
            # print("kill ", self.process.pid, self.process.returncode)
            self.running = False
            if platform.system() == "Windows":
                p = subprocess.Popen("taskkill /F /T /PID %i" % self.process.pid, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                while p.poll() is None:
                    line = p.stdout.readline()
                    # print('>>', line)
            else:
                os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)

if __name__ == "__main__":
    # for test
    # cmd = "pio run -t upload"
    cmd = [
        "pio init --board uno", 
        "pio run -t upload"
    ]
    env = {
        "PATH": "E:/kittenblock/python/win/Scripts",
        "PLATFORMIO_CORE_DIR": "E:/kittenblock/python/pio"
    }
    cwd = "E:/kittenblock/python/test"
    # def onOutput(msg):
    #     print(">>", msg)
    # def onFinish(code):
    #     print("Done %s" %code)
    th = ExecThread(cmd, cwd, onOutput, onFinish, env)
    th.setDaemon(True)
    th.start()

    a = input()
