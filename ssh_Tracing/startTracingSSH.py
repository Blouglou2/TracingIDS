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
import hashlib

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
            # exit_status = stdout.channel.recv_exit_status()
            print( "%s launched. \n" %(command))
        else:
            print("Connection not opened.")

    def sendBlockingCommand(self, command):
        if(self.client):
            print("Launching command %s \n" %(command))
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            print(stdin)
            print(exit_status)
            print( "%s launched in blocking mode. \n" %(command))
            return(stdout)
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
    connection.sendCommand("mkdir infected")
    connection.sendCommand("chmod u+x infected/")
    print(datetime.now().time())
    connection.sendCommand("sleep(1)")
    connection.sendCommand("rm -r test/")
    print("Intrusion réussie")

def intrusionInfectedsh(connection):
    print("Intrusion infected.sh")
    connection.sendCommand("./infected.sh")
    print(datetime.now().time())
    print("Intrusion réussie")

def intrusionChiffrement(connection):
    print("Intrusion chiffrement")

    # password = 'CleDeChiffrementBaby'.encode("utf-8")
    # key = hashlib.sha256(password).hexdigest()
    # with open("../attaques/cleChiffrement.txt","w") as fichierCle:
    #     fichierCle.write(key[:32])
    #     print("Cle enregistrée!")

    connection.sendBlockingCommand("python3 AESCrypto.py -k cleChiffrement.txt -i textesAChiffrer/ -m c")
    print(datetime.now().time())
    print("Intrusion réussie")

def dechiffreIntrusionChiffrement(connection):
    print("Intrusion chiffrement")
    # with open("../attaques/cleChiffrement.txt","w") as fichierCle:
    #     fichierCle.write(key[:32])
    #     print("Cle enregistrée!")

    connection.sendCommand("python3 AESCrypto.py -k cleChiffrement.txt -i textesAChiffrer/ -m d")
    print(datetime.now().time())
    print("Déchiffrement réussi")

def intrusionEspionnage(connection):
    print("Intrusion expionnage")
    connection.sendCommand("python3 ./espionnage.py")
    print(datetime.now().time())
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

def benchmarkRpi():
    
    # for delais in ["0.5","1","2","3","4","5","10"]:
        
    #     with open("../benchmarkRpi.txt","a") as fichierOutput:
    #             fichierOutput.write("\n-------------------------------------------------------------------------\n")
    #             fichierOutput.write("Traçage "+ str(delais)+" :")

    #     for repetition in range(11):
    #         connection = ssh(ipToTrace,login,password)
    #         time.sleep(3)

    #         connection.sendCommand("sudo ./startTracing.sh "+str(delais))

    #         stdout = connection.sendBlockingCommand("sysbench --test=cpu --cpu-max-prime=20000 run ")
    #         output = str(stdout.read(),"utf-8")
            
    #         connection.sendCommand("\x003")
    #         connection.sendCommand("sudo ~/stopTracing.sh")

    #         with open("../benchmarkRpi.txt","a") as fichierOutput:
    #             fichierOutput.write("\n")
    #             fichierOutput.writelines(output)

    #         time.sleep(8)
    #         os.system('rm -rf /home/robin/Bureau/TestMachineLearning/HomeAssistant/infecte2/hassbian/*')

    #         connection.sendCommand("sudo reboot")

    #         connection.closeConnection()

    #         time.sleep(120)
    # for delais in ["0.5","1","2","3","4","5","10"]:
            
    #         with open("../benchmarkRpi.txt","a") as fichierOutput:
    #                 fichierOutput.write("\n-------------------------------------------------------------------------\n")
    #                 fichierOutput.write("\n-------------------------------------------------------------------------\n")
    #                 fichierOutput.write("\n-------------------------Memoire-----------------------------------------\n")
    #                 fichierOutput.write("\n-------------------------------------------------------------------------\n")
    #                 fichierOutput.write("\n-------------------------------------------------------------------------\n")
    #                 fichierOutput.write("Traçage "+ str(delais)+" :")

    #         for repetition in range(11):
    #             connection = ssh(ipToTrace,login,password)
    #             time.sleep(3)

    #             connection.sendCommand("sudo ./startTracing.sh "+str(delais))

    #             stdout = connection.sendBlockingCommand("sysbench --test=memory --memory-total-size=10G run ")
    #             output = str(stdout.read(),"utf-8")
                
    #             connection.sendCommand("\x003")
    #             connection.sendCommand("sudo ~/stopTracing.sh")

    #             with open("../benchmarkRpi.txt","a") as fichierOutput:
    #                 fichierOutput.write("\n")
    #                 fichierOutput.writelines(output)

    #             time.sleep(8)
    #             os.system('rm -rf /home/robin/Bureau/TestMachineLearning/HomeAssistant/infecte2/hassbian/*')

    #             connection.sendCommand("sudo reboot")

    #             connection.closeConnection()

    #             time.sleep(120)

    
    with open("../benchmarkRpi.txt","a") as fichierOutput:
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")
                    fichierOutput.write("\n---------------------Sans Tracage CPU------------------------------------\n")
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")

    for repetition in range(11):
                connection = ssh(ipToTrace,login,password)
                time.sleep(3)

                stdout = connection.sendBlockingCommand("sysbench --test=cpu --cpu-max-prime=20000 run ")
                output = str(stdout.read(),"utf-8")

                with open("../benchmarkRpi.txt","a") as fichierOutput:
                    fichierOutput.write("\n")
                    fichierOutput.writelines(output)


    with open("../benchmarkRpi.txt","a") as fichierOutput:
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")
                    fichierOutput.write("\n---------------------Sans Tracage Memoire--------------------------------\n")
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")
                    fichierOutput.write("\n-------------------------------------------------------------------------\n")

    for repetition in range(11):
                connection = ssh(ipToTrace,login,password)
                time.sleep(3)

                stdout = connection.sendBlockingCommand("sysbench --test=memory --memory-total-size=10G run ")
                output = str(stdout.read(),"utf-8")

                with open("../benchmarkRpi.txt","a") as fichierOutput:
                    fichierOutput.write("\n")
                    fichierOutput.writelines(output)

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
        3. Intrusion Infected.sh
        4. Stopper tracage
        5. Supprimer traces  
        6. Intrusion ransomware
        7. Intrusion espionnage
        8. Quit
        9. Déchiffrer ransomware
        10. Benchmarks Rpi
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
            lancerTracage(connection)
            time.sleep(10)
            intrusionInfectedsh(connection)
            time.sleep(2)
            stopperTracage(connection)
        elif ans == "4":
            stopperTracage(connection)
        elif ans == "5":
            suppressionTraces()
        elif ans == "6":
            lancerTracage(connection)
            time.sleep(10)
            intrusionChiffrement(connection)
            time.sleep(2)
            stopperTracage(connection)
        elif ans == "7":
            lancerTracage(connection)
            time.sleep(10)
            intrusionInfectedsh(connection)
            time.sleep(2)
            stopperTracage(connection)
        elif ans == "8":
            break
        elif ans== "9":
            dechiffreIntrusionChiffrement(connection)
        elif ans== "10":
            benchmarkRpi()
        elif ans !="" :
            print("Ce choix n'est pas correct")
    
if __name__ == "__main__":
    main()