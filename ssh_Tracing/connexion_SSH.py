from paramiko import client
import time
import babeltrace
import babeltrace.reader
from babeltrace import *
# except ImportError:          # quick fix for debian-based distros
#     sys.path.append("/usr/local/lib/python%d.%d/site-packages" % (sys.version_info.major, sys.version_info.minor))
#     from babeltrace import *

import sys
import os
from stat import ST_CTIME

from handlerCreationTrace import *


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
            # while not stdout.channel.exit_status_ready():
            #     # Print data when available
            #     if stdout.channel.recv_ready():
            #         alldata = stdout.channel.recv(1024)
            #         prevdata = b"1"
            #         while prevdata:
            #             prevdata = stdout.channel.recv(1024)
            #             alldata += prevdata
 
            #         print(str(alldata, "utf8"))
            print( "%s launched. \n" %(command))
        else:
            print("Connection not opened.")


# def babeltraceReading(directory): # Lit les traces d'un snapshot
#     # directory = "."
#     directoryList = dateSort(directory)
#     lastTraceDirectory = directoryList[0]  # Ajouter kernel?
    
#     trace_collection = babeltrace.reader.TraceCollection()

#     trace_collection.add_trace(lastTraceDirectory, 'ctf')

#     for event in trace_collection.events:
#         print(event.name)



# def dateSort(directory):
#     files = [(os.stat(f)[ST_CTIME], f) for f in os.listdir(directory) if os.path.isfile(f)]
#     files.sort(reverse= True)
#     return  [f for s,f in files]




def main():
    severiteMenaceDetectee = 0
    connection = ssh("169.254.147.178", "root", "azerty")
    connection.sendCommand("~/PRMH2017/startTracing.sh")
    while severiteMenaceDetectee == 0 :
        mdpe = input("Menace détectée avec Babeltrace? : ")
        severiteMenaceDetectee = 1
        # time.sleep(5)
        # print("Lecture des traces avec babeltrace \n")
        # babeltraceReading("../VMarm1/")
        # print("\n\n---------------------------------------------------\n\n")
    else:
        connection.sendCommand("~/stopTracing.sh")
        time.sleep(10)  # On attend la fin du traçage
        connection.sendCommand("~/startTracing.sh")
        ################## TODO : programme babeltrace qui lit les snapshots et qui modifie la valeur de severteMenaceDetectee pour changer le profil de traçage
    mdpe = input("Appuyer sur une touche pour arrêter le traçage : ")
    connection.sendCommand("~/stopTracing.sh")
    
if __name__ == "__main__":
    main()