import baseDeDonne
import testFeatureExtraction
import re
import sqlite3
import sys


class infosIP(object):
    def __init__(self):
        self.portSource=0
        self.portDest=0
        self.ipSource=0
        self.ipDest=0


def processIPnet_dev_queue_(event):
    # TODO on vérifie qu'on est avec le bon event sinon on jette une erreur, a priori aps besoin de check la nature de l'event vu qu'on ne apsse que les bons events

    portSource=0
    portDest=0
    ipSource=0
    ipDest=0
    try:
        if event["source_port"] :
            portSource = event["source_port"]
        if event["dest_port"] :
            portDest = event["dest_port"]
        if event["saddr"] :
            ipSource = event["saddr"]
        if event["daddr"] :
            ipDest = int(event["daddr"])
    except KeyError:
        pass
    
    # if "source_port" in event["network_header"]["transport_header"].keys():
    #     portSource = event["network_header"]["transport_header"]["source_port"] 
    # if "dest_port" in event["network_header"]["transport_header"].keys():
    #     portDest = event["network_header"]["transport_header"]["dest_port"]
    # ipSource =  ".".join(str(x) for x in event["network_header"]["saddr"]) 
    # ipDest =  ".".join(str(x) for x in event["network_header"]["daddr"])
    infosIP.portSource=portSource
    infosIP.portDest=portDest
    infosIP.ipSource=ipSource
    infosIP.ipDest=ipDest
    
    return infosIP
    # if (portSource and portDest and ipSource and ipDest):
    #     print("PortSource : ",portSource ," | ","PortDest : ",portDest," | ","ipSource : ",ipSource," | ","ipDest : ",ipDest )
    # else:
    #     print("ipSource : ",ipSource," | ","ipDest : ",ipDest )
    

        
def addIPBDD(event):

    baseDeDonne.initialisationDB("./data/database.db")
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()
    infoIP = infosIP()
    infoIP = processIPnet_dev_queue_(event)
    # print("PortSource : ",infoIP.portSource ," | ","PortDest : ",infoIP.portDest," | ","ipSource : ",infoIP.ipSource," | ","ipDest : ",infoIP.ipDest )
    cursor.execute(""" 
    INSERT OR IGNORE INTO ip(IPdevice,IPdest,PortSource,PortDest)
    VALUES(?,?,?,?)""",(infoIP.ipSource,infoIP.ipDest,infoIP.portSource,infoIP.portDest)
    )

    db.commit()

    baseDeDonne.closeDB(db)


def addFilenameBDD(event):

    baseDeDonne.initialisationDB("./data/database.db")
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()
    cursor.execute(""" 
    INSERT OR IGNORE INTO filename(evenement,filename)
    VALUES(?,?)""",(event["a_nomEvent"],event["filename"])
    )

    db.commit()

    baseDeDonne.closeDB(db)

def addParentChildBDD(event):

    baseDeDonne.initialisationDB("./data/database.db")
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()
    cursor.execute(""" 
    INSERT OR IGNORE INTO parentChild(parent,child)
    VALUES(?,?)""",(event["parent_comm"],event["child_comm"])
    )

    db.commit()

    baseDeDonne.closeDB(db)



def checkIPBDD(event):
    """ Retourne 1 si une IP n'est pas présente dans la BDD """
    # TODO erreur si la BDD n'existe pas
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()

    infoIP = infosIP()
    infoIP = processIPnet_dev_queue_(event)


    cursor.execute("SELECT rowid FROM ip WHERE (IPdest = ? AND PortSource = ? AND PortDest = ?)", (infoIP.ipDest,infoIP.portSource,infoIP.portDest))
    data=cursor.fetchall()
    if len(data)==0:
        # print("L'IP ", infoIP.ipDest, "n'est pas autorisée à communiquer avec l'appareil")
        return 1
    else:
        # print("L'IP est valide dans la BDD")
        return 0

def checkfilenameBDD(event):
    """ Retourne 1 si une IP n'est pas présente dans la BDD """
    # TODO erreur si la BDD n'existe pas
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()

    cursor.execute("SELECT rowid FROM filename WHERE (evenement = ? AND filename = ? )", (event["a_nomEvent"],event["filename"]))
    data=cursor.fetchall()
    if len(data)==0:
        # print("Ce nom de fichier n'a aps le droit d'êter appelé par cet évènement")
        return 1
    else:
        # print("Cet évènement peut appeler ce fichier")
        return 0


def checkParentChildBDD(event):
    """ Retourne 1 si une IP n'est pas présente dans la BDD """
    # TODO erreur si la BDD n'existe pas
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()

    cursor.execute("SELECT rowid FROM parentChild WHERE (parent = ? AND child = ? )", (event["parent_comm"],event["child_comm"]))
    data=cursor.fetchall()
    if len(data)==0:
        # print("Ce nom de fichier n'a aps le droit d'êter appelé par cet évènement")
        return 1
    else:
        # print("Cet évènement peut appeler ce fichier")
        return 0

def addRegleAbsolues(event):

    # if (re.search("net_dev_queue",event.name)):
        # addIPBDD(event)  
        checkIPBDD(event)

def main():
    adresse = sys.argv[1]

    # processAdresse(adresse)

if __name__ == '__main__':
    main()