#!/usr/bin/env python
import argparse
import threading
import paramiko
import subprocess
import multiprocessing
from multiprocessing import Process, Queue, Manager
import getpass
from queue import Queue
import time
import socket

# set up global variables
found_ports={}

# set up threading
print_lock = threading.Lock()

# Create the queue and threader 
q = Queue()

# need to set up the main parser and threading

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='scan',
                                    add_help=True,
                                    description='A multi-process service scanner')
    parser.add_argument('-file','-f', help='location of wordlist')
    parser.add_argument('-ip','-i',help='Target IP Address')
    parser.add_argument('-user','-u', nargs='*',help='username')

    args = parser.parse_args()
