#!/usr/bin/env python
import threading
from queue import Queue
import time
import socket
import argparse
import sys
# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()
# create a global dictionary
found_ports={}
#target = ''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='scan',
                                    add_help=True,
                                    description='A multi-process service scanner')
    #parser.add_argument('-file','-f', help='location of wordlist')
    parser.add_argument('-ip','-i',help='Target IP Address')
    #parser.add_argument('-user','-u', nargs='?',help='username')
    if len(sys.argv)<2:
        print('Must use -ip xxx.xxx.xxx.xxx flag')
        sys.exit()
    args = parser.parse_args()
    print(args.ip)
    global target 
    target = args.ip


#target = '104.248.191.147'
#ip = socket.gethostbyname(target)
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(.4)
    try:
        con = s.connect((target,port))
        with print_lock:
            found_ports.update(port=socket.getservbyport(port))
            print('{} - {}'.format(port,socket.getservbyport(port)))
        con.close()
    except:
        pass
# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()
        # Run the example job with the avail worker in queue (thread)
        portscan(worker)
        # completed with the job
        q.task_done()
# Create the queue and threader 
q = Queue()
# how many threads are we going to allow for
for x in range(1000):
     t = threading.Thread(target=threader)
     # classifying as a daemon, so they will die when the main dies
     t.daemon = True
     # begins, must come after daemon definition
     t.start()
start = time.time()
# 100 jobs assigned. 65535
for worker in range(1,65535):
    q.put(worker)
# wait until the thread terminates.
q.join()
