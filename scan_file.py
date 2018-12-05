#!/usr/bin/env python
import argparse
import threading
import paramiko
import subprocess
import multiprocessing
from multiprocessing import Process, Queue, Manager
import getpass

def connect_to_ip(args):
    ssh_command(args.ip,'jason','jason1977','ClientConnected')
    # for user in args.user:
    #     file=open(args.file,'r')
    #     data = file.readlines()
    #     for line in data:
    #         try:
    #             passwd=line.strip()
    #             # print(str(args.ip) + ' ' + str(user) + ' ' + passwd + ' ClientConnected')
    #             # ssh_command(args.ip,user,passwd,'ClientConnected')
    #             p = multiprocessing.Process(target=ssh_command, args=(args.ip,user,passwd,'ClientConnected',))
    #             p.start()
    #         except:
    #             pass
    #     file.close()
    
def ssh_command2(ssh):
    command = input("Command:")
    #ssh.invoke_shell()
    #stdin, stdout, stderr = ssh.exec_command(command)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    #print(stdout.read())
    while not ssh_stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
        if ssh_stdout.channel.recv_ready():
            rl, wl, xl = select.select([ssh_stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                # Print data from stdout
                print(ssh_stdout.channel.recv(1024),)

    #
    # Disconnect from the host
    #
    print("Command done, closing SSH connection")
    client.close()

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #calling paramiko
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        try:
            client.connect(hostname=ip, username=user, password=passwd)
            ssh_command2(client)
            break
            # ssh_session = client.get_transport().open_session()
            # print("DEBUG1")
            # if ssh_session.active:
            #     ssh_session.exec_command(command)
            #     #print(ssh_session.recv(1024)) #read banner
            #     try:
            #         command = ssh_session.recv(1024)
            #         print("Successful login: User: {} Password: {}".format(user,passwd))
            #         while True:
            #             command = ssh_session.recv(1024) #get the command from the SSH server
            #             ssh_command(client)
            #             try:
            #                 pass
            #             except Exception as e:
            #                 pass
            #                 #ssh_session.send(str(e))
            #     except:
            #         client.close()
            #         pass
            #         #ssh_session.send(str(e))
                
            #     client.close()
        except Exception as e:
            # print(str(e))
            client.close()
            pass
        return
    # Wait for the command to terminate
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='scan',
                                    add_help=True,
                                    description='A multi-process service scanner')
    parser.add_argument('-file','-f', help='location of wordlist')
    parser.add_argument('-ip','-i',help='Target IP Address')
    parser.add_argument('-user','-u', nargs='*',help='username')

    args = parser.parse_args()
    connect_to_ip(args)
    #print(args)