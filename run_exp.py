import os
import psutil
import subprocess
import time
import argparse

CMD_W_EXT  = ['google-chrome', '--user-data-dir=/home/testbed/Desktop/tool4autoload/default_profile/']
CMD_WO_EXT = ['google-chrome', '--disable-extensions', '--user-data-dir=/home/testbed/Desktop/tool4autoload/default_profile/']

PATH_TO_URLLIST = '/home/testbed/Desktop/tool4autoload/urllist.txt'
RUNS_WITH_EXT = True

TIMEOUT_PAGE_LOAD = 60

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--extension", action="store_true")
parser.add_argument("-t", "--timeout", action='store', type=int)
parser.add_argument("-pp", "--user_path", action='store', type=str)
args = parser.parse_args()

TIMEOUT_PAGE_LOAD = args.timeout
RUNS_WITH_EXT = args.extension
CMD_W_EXT[-1] = '--user-data-dir=' + args.user_path
CMD_WO_EXT[-1] = '--user-data-dir=' + args.user_path

def kill_child_processes(parent_pid):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        print '[ERROR] No such process with PID ' + str(parent_pid)
        return
    for child in parent.children(recursive=True):
        try:
            child.kill()
        except psutil.NoSuchProcess:
            print '[ERROR] No such process with PID ' + str(child.pid)
            continue
    parent.kill()

def read_urllist(path):
    with open(path) as file:
        urllist = file.readlines()
    urllist = map(lambda l: l[:-1], urllist)
    return urllist

def open_url(url, runs_w_ext):
    print '[INFO] Now loading ' + url + '...'
    if runs_w_ext:
        p = subprocess.Popen(args=CMD_W_EXT + [url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    else:
        p = subprocess.Popen(args=CMD_WO_EXT + [url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    return p

if __name__ == '__main__':
    urllist = read_urllist(PATH_TO_URLLIST)
    list_size = len(urllist)
    for i in range(list_size):
        p_browser = open_url(urllist[i], RUNS_WITH_EXT)
        time.sleep(TIMEOUT_PAGE_LOAD)
        p_browser.terminate()
        kill_child_processes(p_browser.pid)
        print '[INFO] Done. ' + str(list_size-(i+1)) + '/' + str(list_size) + ' to go!'
        print ''
