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
        self.proto=0


def processIPnet_dev_queue_(event):
    # TODO on vérifie qu'on est avec le bon event sinon on jette une erreur, a priori aps besoin de check la nature de l'event vu qu'on ne apsse que les bons events

    portSource=0
    portDest=0
    ipSource=0
    ipDest=0
    proto = 0
    try:
        if event["source_port"] :
            portSource = event["source_port"]
        if event["dest_port"] :
            portDest = event["dest_port"]
        if event["saddr"] :
            ipSource = int(event["saddr"])
        if event["daddr"] :
            ipDest = int(event["daddr"])
        if event["protocol"] :
            proto = int(event["protocol"])
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
    infosIP.proto=proto
    
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
    INSERT OR IGNORE INTO ip(IPdevice,IPdest,PortSource,PortDest,NomProcessus,Protocole)
    VALUES(?,?,?,?,?,?)""",(infoIP.ipSource,infoIP.ipDest,infoIP.portSource,infoIP.portDest,event["p_name"],infoIP.proto)
    )

    db.commit()

    baseDeDonne.closeDB(db)


def addFilenameBDD(event):

    baseDeDonne.initialisationDB("./data/database.db")
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()
    cursor.execute(""" 
    INSERT OR IGNORE INTO filename(evenement,filename,NomProcessus,ret)
    VALUES(?,?,?,?)""",(event["a_nomEvent"],event["filename"],event["p_name"],event["ret"])
    )

    db.commit()

    baseDeDonne.closeDB(db)

def addPathnameBDD(event):
    
    baseDeDonne.initialisationDB("./data/database.db")
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()
    cursor.execute(""" 
    INSERT OR IGNORE INTO pathname(evenement,pathname,NomProcessus,ret)
    VALUES(?,?,?,?)""",(event["a_nomEvent"],event["pathname"],event["p_name"],event["ret"])
    )

    db.commit()

    baseDeDonne.closeDB(db)

def addParentChildBDD(event):

    baseDeDonne.initialisationDB("./data/database.db")
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()
    cursor.execute(""" 
    INSERT OR IGNORE INTO parentChild(parent,child,NomProcessus)
    VALUES(?,?,?)""",(event["parent_comm"],event["child_comm"],event["p_name"])
    )

    db.commit()

    baseDeDonne.closeDB(db)

def addSyscallBDD(event):
    
    baseDeDonne.initialisationDB("./data/database.db")
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()
    cursor.execute(""" 
    INSERT OR IGNORE INTO syscall(evenement,NomProcessus,ret)
    VALUES(?,?,?)""",(event["a_nomEvent"],event["p_name"],event["ret"])
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


    cursor.execute("SELECT rowid FROM ip WHERE (IPdest = ? AND PortSource = ? AND PortDest = ? AND NomProcessus = ?)", (infoIP.ipDest,infoIP.portSource,infoIP.portDest,event["p_name"]))
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

    cursor.execute("SELECT rowid FROM filename WHERE (evenement = ? AND filename = ? AND NomProcessus = ? AND ret = ?)", (event["a_nomEvent"],event["filename"],event["p_name"],event["ret"]))
    data=cursor.fetchall()
    if len(data)==0:
        # print("Ce nom de fichier n'a aps le droit d'êter appelé par cet évènement")
        return 1
    else:
        # print("Cet évènement peut appeler ce fichier")
        return 0

def checkPathnameBDD(event):
    """ Retourne 1 si une IP n'est pas présente dans la BDD """
    # TODO erreur si la BDD n'existe pas
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()

    cursor.execute("SELECT rowid FROM pathname WHERE (evenement = ? AND pathname = ? AND NomProcessus = ? AND ret = ?)", (event["a_nomEvent"],event["pathname"],event["p_name"],event["ret"]))
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

    cursor.execute("SELECT rowid FROM parentChild WHERE (parent = ? AND child = ? AND NomProcessus = ?)", (event["parent_comm"],event["child_comm"],event["p_name"]))
    data=cursor.fetchall()
    if len(data)==0:
        # print("Ce nom de fichier n'a pas le droit d'êter appelé par cet évènement")
        return 1
    else:
        # print("Cet évènement peut appeler ce fichier")
        return 0

def checkSyscallBDD(event):
    """ Retourne 1 si une IP n'est pas présente dans la BDD """
    # TODO erreur si la BDD n'existe pas
    db = sqlite3.connect("./data/database.db")

    cursor = db.cursor()

    cursor.execute("SELECT rowid FROM syscall WHERE (evenement = ? AND NomProcessus = ? AND ret = ?)", (event["a_nomEvent"],event["p_name"],event["ret"]))
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