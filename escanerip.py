import ipaddress
import os
from datetime import datetime
import platform
import re
import socket
import time
import threading
from queue import Queue


puertotot = 0
tiempo = datetime.now()
espero = threading.Lock()
socket.setdefaulttimeout(0.25)
ipsactivas = 0
# Listas
listaipvalidar = []
lista2ping = []


########################################################################### PING a IPs validas
def ping(ipvalida):
    global ipsactivas
    if platform.system().lower() == 'windows':
        response = os.system('ping -n 1 -w 500 ' + ipvalida + ' > nul')
        if response == 0:
            lista2ping.append(ipvalida)
            ipsactivas += 1
    if platform.system().lower() == 'linux':
        response = os.system('ping -c 1 -W 1 ' + ipvalida + '> /dev/null')
        if response == 0:
            lista2ping.append(ipvalida)
            ipsactivas += 1


###############################################################################


###########################################################################  VALIDAR IP
def validate_ipaddress(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError as errorCode:

        pass
        return False


def main():
    global ipno
    global ipaddr
    ipno = False
    ipaddr = input("Ingresar ip: \n")
    while ipno != True:
        if (validate_ipaddress(ipaddr) == False):
            print(" IP INVALIDA ")
            ipno = False
            ipaddr = input("Ingresar ip:\n")
        else:
            print("IP {} valida".format(ipaddr))
            ipno = True
        # ipaddr = input("Ingresar ip o (q para salir):\n")


if __name__ == "__main__":
    main()
##################################################################################

################################################################################# Cantidad de IPs
while True:
    print("################################################")
    cantidadip = input("Cantidad de IPs: ")
    print('################################################')
    if cantidadip.isdecimal() == False:
        print("La cantidad debe ser un numero y entero. ")
        continue
    break
#################################################################################


################################################################################# Todas las IPs a escanear
if cantidadip.isdecimal() == True:
    cantidadip = int(cantidadip)
cant = 0
while cant < cantidadip:
    listaipvalidar.append(ipaddr)
    suma = int(ipaddress.IPv4Address(ipaddr))
    suma = suma + 1
    ipaddr = str(ipaddress.IPv4Address(suma))
    cant = cant + 1
cantenlistaip1 = len(listaipvalidar)
###################################################################################

################################################################################### Hago ping a las ips a escanear
hacerping = 0
while hacerping < cantenlistaip1:
    hacer = listaipvalidar[hacerping]
    ping(hacer)
    hacerping += 1
ipspinglista = len(lista2ping)
pinglisto = 0
if pinglisto < ipspinglista:
    print('IPs Activas: ')
    while pinglisto < ipspinglista:
        print(lista2ping[pinglisto])
        pinglisto += 1
    print('################################################')
    print('')


#####################################################################################

##################################################################### Puertos

def escaneo(port, pasoip):
    global puertotot
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conecto = s.connect((pasoip, port))
        with espero:
            print(pasoip, port, ' puerto abierto')
            puertotot += 1
        conecto.close()
    except:
        pass


def threader():
    while True:
        trabajador = queu1.get()
        escaneo(trabajador, pasoip)
        queu1.task_done()


queu1 = Queue()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

ippuerto = 0
while ippuerto < ipspinglista:
    pasoip = lista2ping[ippuerto]
    for trabajador in range(1, 500):
        queu1.put(trabajador, pasoip)
    ippuerto += 1
    queu1.join()

#################################################################################
# tiempo de programa
print('')
print('IPs Activas: ', ipsactivas)
print('Puertos totales:', puertotot)
tiempo_trans = datetime.now() - tiempo
print('El programa finalizo en {}'.format(tiempo_trans))
