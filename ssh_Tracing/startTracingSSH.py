from paramiko import client
import time
import babeltrace
import babeltrace.reader
from babeltrace import *

import sys
import os
from stat import ST_CTIME

from handlerCreationTrace import *

from datetime import datetime

ipToTrace="132.207.72.35"
login="pi"
password="raspberry"




class ssh:
    client = None
 
    def __init__(self, address, username, password):
        print("Connecting to server. \n")
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        print("Connection success. \n")
 
    def sendCommand(self, command):
        if(self.client):
            print("Launching command %s \n" %(command))
            stdin, stdout, stderr = self.client.exec_command(command)
            print( "%s launched. \n" %(command))
        else:
            print("Connection not opened.")

    def closeConnection(self):
        self.client.close()
        print("Connection closed. \n")


def lancerTracage(connection):
    print("Lancement du traçage")
    input("lttng-relayd est-il bien lancé?")
    delais = input("Delais pour les snapshots : ")
    connection.sendCommand("sudo ./startTracing.sh "+str(delais))
    print("Traçage lancé")

def intrusionMkdir(connection):
    print("Intrusion mkdir -> chmod -> rm")
    connection.sendCommand("mkdir test")
    connection.sendCommand("chmod u+x test/")
    print(datetime.now().time())
    connection.sendCommand("sleep(1)")
    connection.sendCommand("rm -r test/")
    print("Intrusion réussie")

def stopperTracage(connection):
    print("Arret du traçage")
    connection.sendCommand("\x003")
    connection.sendCommand("sudo ~/stopTracing.sh")
    print("Tracage terminé")
    print("En attente des dernier snapshots...")
    time.sleep(8)   # Pour être sûr d'avoir reçu les derniers snapshots
    print("Chown sur les snapshots...")
    os.system('sudo chown -R robin:robin hassbian/')

def suppressionTraces():
    print("Suppression des traces ")
    os.system('rm -rf ~/Bureau/TestMachineLearning/HomeAssistant/hassbian/*')
    print("Traces supprimées")

def main():
    connection = ssh(ipToTrace,login,password)

    ans = True
    while ans:
        print("""
        ##################################
        ##                              ##
        ##    Tracage sur le device     ##
        ##                              ##
        ##################################

        1. Lancer traçage
        2. Intrusion mkdir (inclus le lancement et l'arrêt du traçage)
        3. Stopper tracage
        4. Supprimer traces  
        5. Quit
         """)

        ans = input()
        if ans == "1":
            lancerTracage(connection)
        elif ans == "2":
            lancerTracage(connection)
            time.sleep(10)
            intrusionMkdir(connection)
            time.sleep(2)
            stopperTracage(connection)
        elif ans == "3":
            stopperTracage(connection)
        elif ans == "4":
            suppressionTraces()
        elif ans == "5":
            break
        elif ans !="" :
            print("Ce choix n'est pas correct")
    
if __name__ == "__main__":
    main()