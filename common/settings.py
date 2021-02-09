import time
import os
import subprocess

FILE_TRANSFER = ""

def ip4_addresses():
    words = subprocess.run(["netstat", "-rn"], stdout=subprocess.PIPE)
    words = str(words).split()
    list_ips = []
    for x in words:
        if "192." in x:
            y = x[x.find("192."):]
            if y.count(".") == 3 and y not in list_ips:
                list_ips.append(y)
        if "25." in x:
            y = x[x.find("25."):]
            if y.count(".") == 3 and y not in list_ips:
                list_ips.append(y)
        if "127." in x:
            y = x[x.find("127."):]
            if y.count(".") == 3 and y not in list_ips:
                list_ips.append(y)
    
    return list_ips
    
    
def choose_ip(ip_list):
    i=0
    for ip in ip_list:
        print(f"[{i}] : {ip}")
        i+=1
    ip = input("Pick the ip you want to use!\nIf you want to use a different IP please type it here: ")
    try:
        num = int(ip)
    except Exception:
        return ip
    return ip_list[num]

SERVER_IP = ""
MY_IP = ""
MY_NAME = ""

def init(name):
    global SERVER_IP, MY_IP, MY_NAME
    MY_NAME = name
    ip_list = ip4_addresses()
    MY_IP = choose_ip(ip_list)
    os.system('clear')
    if MY_NAME.lower() != "server":
        print("Hello {}, Your chosen ip is: {}".format(MY_NAME, MY_IP))
        SERVER_IP = input("Please enter server ip address: ")
    else:
        print("Hello server, other players can connect to game using: {}".format(MY_IP))
        SERVER_IP = MY_IP