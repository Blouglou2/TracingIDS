#!/usr/bin/env python
# -*- coding :ascii -*-

import re
import constructionBDD


### Vieilles règles ###
def reglesFilename(event):
    category= 0
    try:
        if re.search("/bin/rm",event["filename"]) or re.search("/bin/mkdir",event["filename"]) or re.search("/bin/chmod",event["filename"]) :
            category = 1
    except KeyError:
        category = 0
    return category

def reglesNomEvent(event):
    category = 0
    try:
        if re.search("geteuid",event["a_nomEvent"]) or re.search("mkdir",event["a_nomEvent"]):
            category = 1
    except KeyError:
        category = 0
    return category


### Règles BDD ###
def reglesNetDevQueue(event):
    category = 0
    if re.search("net_dev_queue",event["a_nomEvent"]): 
        
        infoIP = constructionBDD.infosIP()
        infoIP = constructionBDD.processIPnet_dev_queue_(event)
        # print(infoIP.ipDest)
        if constructionBDD.checkIPBDD(event):
            category = 1
        return category
    else:
        return category

def reglesFilename(event):
    category = 0
    try:
        if event["filename"]:
            if constructionBDD.checkfilenameBDD(event):
                category = 1
    except KeyError:
            pass
    return category

def reglesParentChild(event):
    category = 0
    try:
        if event["child_comm"] and event["parent_comm"]:
            if constructionBDD.addParentChildBDD(event):
                category = 1
    except KeyError:
            pass
    return category







def reglesLabelisation(event):
    category = 0
    # category = reglesFilename(event)
    # if category == 1:
    #     return category
    # category = reglesNomEvent(event)
    # if category == 1:
    #     return category
    category = reglesNetDevQueue(event)
    if category == 1:
        return category
    category = reglesFilename(event)
    if category == 1:
        return category
    category = reglesParentChild(event)
    if category == 1:
        return category    
    else:
        return category



def main():
    print("main")

if __name__ == '__main__':
    main()













    ################## TODO plus de règles, générer taces normales de hassbian puis attaque et bien labéliser le dataset (peut-être changer la taille des chuncks)