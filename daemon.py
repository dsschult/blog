#!/usr/bin/env python

import sys
import os
import signal
import time
import subprocess


def find_processes(name):
    ret = []
    out = subprocess.check_output(['ps','aux'])
    for line in out.split('\n'):
        if name in line:
            ret.append(int(line.split()[1]))
    return ret

def kill_processes(pids):
    for pid in pids:
        os.kill(pid, signal.SIGINT)
    time.sleep(2)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except Exception:
            pass

def start():
    subprocess.Popen(['./run.sh'])

def git_checkup():
    return True
    before = subprocess.check_output(['git','log','-n','1']).split()[1]
    subprocess.call(['git','pull'])
    after = subprocess.check_output(['git','log','-n','1']).split()[1]
    if before != after:
        return True
    else:
        return False

if __name__ == '__main__':
    name = 'gunicorn'

    if len(sys.argv) > 1 and sys.argv[1] == 'stop':
        print('stopping')
        p = find_processes(name)
        print(p)
        if p:
            kill_processes(p)
    else:
        if git_checkup():
            print('restarting')
            p = find_processes(name)
            print(p)
            if p:
                kill_processes(p)
            start()
