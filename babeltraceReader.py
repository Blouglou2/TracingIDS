#!/usr/bin/env python
# -*- coding : utf-8 -*-

import babeltrace
import re
import sys
import datetime
# from collections import defaultdict
import collections

import constructionBDD as regles

import syntheticEvents

import reglesLabelisation

def itsADict(event,dictio):
    for key in event:
        if isinstance(event[key],dict):
            itsADict(event[key],dictio)
        
        elif isinstance(event[key],list):
            dictio[key] = int("".join(str(x) for x in event[key]))
            
        else:
            dictio[key]=event[key]
    return dictio

def flattenDict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flattenDict(value).items():
                    yield subkey, subvalue
                # yield flattenDict(value)
            if isinstance(value, list):
                yield key, int("".join(str(x) for x in value))
            else:
                yield key, value

    return dict(items())



def preprocessEventsklearn(event) :
# On sort dictionnaire de la forme {event.name, field1:value,...}
# avec les value qui ne sont que des int ou des str
# ATTENTION : pour les listes on les retire pour l'instant, concerne par exemple uuid

# TODO optimisation? On crée une liste à chaque évènement. Clear mémoire???

    dictEvent = defaultdict(set)
    dictEventtmp={"a_nomEvent" : event.name}
    listeKeyDict=[]
    newdict=0
    for key in event.keys():
        if isinstance(event[key],int) or isinstance(event[key],str):
            dictEventtmp[key] = event[key]

        elif isinstance(event[key],dict):
            newdict = 1
            dictio={}
            out = itsADict(event[key],dictio)
            listeKeyDict.append(dictio)
            # TODO faire les dictionnaires imbriqués avec la fonction d'au-dessus

        elif isinstance(event[key],list):
            # dict2list = {key : int("".join(str(x) for x in event[key]))}
            dict2list = {key : "".join(str(x) for x in event[key])}
            listeKeyDict.append(dict2list)

        else:   # Si liste ou autre
            pass
    
    dictEvent = dictEventtmp.copy()

    if newdict == 1 :
        for d in listeKeyDict:
            for k,v in d.items():
                dictEvent[k] = v

    # print(dictEvent)

    return dictEvent


def preprocessMoreEventsklearn(event, listeMachines,dictTid,dictCPUid) :
# On sort dictionnaire de la forme {event.name, field1:value,...}
# avec les value qui ne sont que des int ou des str

# TODO optimisation? On crée une liste à chaque évènement. Clear mémoire???

    if event.name == "sched_switch":
        # TODO COMPLETER
        try:
            dictTid[event["next_tid"]]= event["next_comm"]
            dictTid[event["prev_tid"]]= event["prev_comm"]
            dictCPUid[event["cpu_id"]] = event["next_comm"]
        except KeyError:
            pass
        return {}
    
    
    dictEvent = collections.defaultdict(set)
    # dictEventtmp={"a_nomEvent" : event.name}
    listeKeyDict=[]
    newdict=0
    # category = 9

    try:

        # dictEvent = flattenDict(event)
        dictEvent = {k:v for k,v in flattenDict(event).items() if k  in ["timestamp_begin","timestamp_end","cpu_id","filename","skbaddr","protocol","stream_instance_id","count","buf","saddr","parent_comm",\
        "daddr","tid","source_port","ret","dest_port","content_size","ack_seq","child_tid","child_pid","id","comm","pathname"]}

        # for key in event.keys():
        #     if isinstance(event[key],int) or isinstance(event[key],str):
        #         dictEventtmp[key] = event[key]

        #     elif isinstance(event[key],dict):
        #         newdict = 1
        #         dictio={}
        #         out = itsADict(event[key],dictio)
        #         listeKeyDict.append(dictio)
        #         # TODO faire les dictionnaires imbriqués avec la fonction d'au-dessus

        #     elif isinstance(event[key],list):
        #         dict2list = {key : int("".join(str(x) for x in event[key]))}
        #         listeKeyDict.append(dict2list)

        #     else:   # Si liste ou autre
        #         pass
    
    except UnicodeDecodeError as unicodeError:
        return {"a_nomEvent" : "erreur_lecture"}

    dictEvent["a_nomEvent"] = event.name
    dictEvent["p_name"] = "hass)0"
    # dictEvent = dictEventtmp.copy()

    # if newdict == 1 :
    #     for d in listeKeyDict:
    #         for k,v in d.items():
    #             dictEvent[k] = int(v)

    
    # print(dictEvent)

    ##### On supprime les champs des events inutiles qui creeraient trop de features avec le one-hot encoder ######
    # TODO quelle est la façon optimale de supprimer des events?
    # dictEvent.pop("uuid",None)    # Valeur de l'uuid trop grandes pour être fit_transofrm?
    # dictEvent.pop("magic",None)
    # dictEvent.pop("packet_size",None)
    # dictEvent.pop("v",None)
    # dictEvent.pop("network_header",None)
    # dictEvent.pop("transport_header",None)


    # dictEvent.pop("daddr_padding",None)
    # dictEvent.pop("saddr_padding",None)
    # dictEvent.pop("fd",None)
    # dictEvent.pop("packet_seq_num",None)
    # dictEvent.pop("uservaddr",None)
    # dictEvent.pop("tos",None)
    # dictEvent.pop("ihl",None)
    # dictEvent.pop("stream_id",None)
    # dictEvent.pop("clone_flags",None)
    # dictEvent.pop("gid",None)
    # dictEvent.pop("value",None)
    # dictEvent.pop("uid",None)
    # dictEvent.pop("addrlen",None)
    # dictEvent.pop("grouplist",None)
    # dictEvent.pop("frag_off",None)
    # dictEvent.pop("bufsiz",None)
    # dictEvent.pop("version",None)
    # dictEvent.pop("euid",None)
    # dictEvent.pop("transport_header_type",None)
    # dictEvent.pop("head",None)
    # dictEvent.pop("size",None)
    # dictEvent.pop("tot_len",None)
    # dictEvent.pop("envp",None)
    # dictEvent.pop("checksum",None)
    # dictEvent.pop("optlen",None)
    # dictEvent.pop("sgid",None)
    # dictEvent.pop("ruid",None)
    # dictEvent.pop("newsp",None)
    # dictEvent.pop("egid",None)
    # dictEvent.pop("level",None)
    # dictEvent.pop("network_header_type",None)
    # dictEvent.pop("gidsetsize",None)
    # dictEvent.pop("optval",None)
    # dictEvent.pop("ovalue",None)
    # dictEvent.pop("which",None)
    # dictEvent.pop("optname",None)


    # dictEvent.pop("timestamp_begin",None)  
    # dictEvent.pop("timestamp_end",None)
    # dictEvent.pop("checksum",None)
    # dictEvent.pop("seq",None)
    # dictEvent.pop("skbaddr",None)
    # dictEvent.pop("id",None)
    # dictEvent.pop("ack_seq",None)
    # try:
    #     del dictEvent["timestamp"]
    # except KeyError:
    #     pass
    dictEvent["d_timestamp"] = dictEvent["timestamp_end"] - dictEvent["timestamp_begin"]
    try:
        dictEvent["p_name"] = dictCPUid[event["cpu_id"]]
    except KeyError:
        pass
    try:
        tid = 0
        if re.search("/proc/[0-9]{1,}",dictEvent["filename"]):
        # if "/proc/" in dictEvent["filename"]:
            tid = int(dictEvent["filename"].split("/")[2])
            dictEvent["filename"] = "/proc/"+dictTid[tid]+"/"+"".join(dictEvent["filename"].split("/")[3:])
    except KeyError:
        pass

    try:
        tid = 0
        if re.search("/proc/[0-9]{1,}",dictEvent["pathname"]):
        # if "/proc/" in dictEvent["pathname"]:
            tid = int(dictEvent["pathname"].split("/")[2])
            dictEvent["pathname"] = "/proc/"+dictTid[tid]+"/"+"".join(dictEvent["pathname"].split("/")[3:])
    except KeyError:
        pass

    dictEvent.pop("timestamp_begin",None)  
    dictEvent.pop("timestamp_end",None)

    # if re.search("syscall",dictEvent["a_nomEvent"]):
    if "syscall" in dictEvent["a_nomEvent"]:
        dictEvent = syntheticEvents.synthetic_EntryExitFromEvent(dictEvent,listeMachines)

    


    # if dictEvent is not None:
    #     category = reglesLabelisation.reglesLabelisation(dictEvent)
        # # print(category)
        

        # # TODO dictEvent["daddr"] est int et pas str, caster?
        # # try:
        # #     if re.search("1322077219",dictEvent["daddr"]):
        # #         category = 0
        # # except KeyError:
        # #     category = 1
    
        # return dictEvent,str(category)
    return dictEvent



def processTraces(trace_path) :

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        if re.search("chmod",event.name) :
            if ('filename' in event.keys()):
                print("Tentative de chmod sur "+event['filename'])
                print(datetime.datetime.now())
            else:
                print("Tentative de chmod")
                print(datetime.datetime.now())
        
        if re.search("faccessat",event.name) :
            if ('filename' in event.keys()):
                if not ( re.search("/etc/ld.so.preload",event['filename']) or re.search("lttng",event['filename'])) :
                    print("Acces a " + event['filename'])
                    if (re.search("chmod",event['filename'])):
                        print(datetime.datetime.now())
                
        # if re.search("execve",event.name) :
        #     if ('filename' in event.keys()):
        #         if not ( re.search("/bin/sleep",event['filename']) or re.search("lttng",event['filename'])) :
        #             print("Execution de " + event['filename'])
        #         if (re.search("chmod",event['filename'])):
        #             print(datetime.datetime.now())

    # print("Fin de l'analyse")



def readAllEvents(trace_path) :

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:

        if re.search("writeback",event.name) :
                print("--")
        else:
            print(event.name)
            for key in event.keys() :
                print("\t",key," : ",event[key])
           

    print("Fin de l'analyse")

def readSyscalls(trace_path) :

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        # print(event.name)

        if re.search("syscall",event.name) :
                print("\n", event.name, " : ")
                for key in event.keys() :
                    print("\t",key," : ",event[key])
    print("Fin de l'analyse")


def read(trace_path) :

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        if (re.search("syscall_entry_access",event.name) or re.search("syscall_entry_newstat",event.name) or re.search("syscall_entry_execve",event.name)) :
            print("\n", event.name, " : ")
            for key in event.keys() :
                print("\t",key," : ",event[key])
    print("Fin de l'analyse")


def readNet(trace_path) :

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        # print(event.name)

        if (re.search("net_dev_queue",event.name)):
                print("\n", event.name, " : ")
                for key in event.keys() :
                    print("\t",key," : ",event[key])
    print("Fin de l'analyse")


def getNet(trace_path) :
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        if (re.search("net_dev_queue",event.name)):
            return event


def getExecve(trace_path) :
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        if (re.search("execve",event.name)):
            yield preprocessEventsklearn(event)


def getSomeExecveNet(trace_path) :
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    compt1=0
    compt2=0
    compt3=0

    for event in trace_collection.events:
        if (re.search("net_dev_queue",event.name) and compt1<10):
            compt1 +=1
            print(preprocessEventsklearn(event))
            yield preprocessEventsklearn(event)

        elif (re.search("execve",event.name) and compt2<10):
            compt2 += 1
            print(preprocessEventsklearn(event))
            yield preprocessEventsklearn(event)

        elif (re.search("execve",event.name) and compt3<10):
            compt3 += 1
            print(preprocessEventsklearn(event))
            yield preprocessEventsklearn(event)



def getExecveNet(trace_path) :
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        if (re.search("net_dev_queue",event.name)):
            print(preprocessMoreEventsklearn(event))
            yield preprocessMoreEventsklearn(event)

        elif (re.search("execve",event.name)):
            print(preprocessMoreEventsklearn(event))
            yield preprocessMoreEventsklearn(event)

        elif (re.search("execve",event.name)):
            print(preprocessMoreEventsklearn(event))
            yield preprocessMoreEventsklearn(event)


def getSomeEventsCSV(trace_path) :
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')
    listeEvents=[]

    listeMachines=[]
    dictTid = {}
    dictCPUid = {}

    for event in trace_collection.events:
        # Le filtrage des events sur fait directement sur le RPI avec startTracing.sh
        try:
            event = preprocessMoreEventsklearn(event,listeMachines,dictTid,dictCPUid)
            if event != {}:
                listeEvents.append(event)
            # print(event)
        except TypeError:
            pass
    # print(listeEvents)
    # print(listeCategory)

    # print([x for x in listeEvents if x is not None])
    return [x for x in listeEvents if x is not None]    # On supprime les évènements vides, qui correspondent à une erreur de lecture Unicode de la part de l'API babeltrace


def printExecveNet(trace_path) :
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    # compt1=0
    # compt2=0
    # compt3=0

    # for event in trace_collection.events:
    #     if (re.search("net_dev_queue",event.name) and compt1<10):
    #         compt1 +=1
    #         print(preprocessEventsklearn(event))

    #     elif (re.search("execve",event.name) and compt2<10):
    #         compt2 += 1
    #         print(preprocessEventsklearn(event))

    #     elif (re.search("execve",event.name) and compt3<10):
    #         compt3 += 1
    #         print(preprocessEventsklearn(event))

    for event in trace_collection.events:
        if (re.search("net_dev_queue",event.name) and 'network_header' in event.keys()):
            print("\n", event.name, " : ")
            for key in event.keys() :
                print("\t",key," : ",event[key])

        elif (re.search("execve",event.name)and 'filename' in event.keys()):
            print("\n", event.name, " : ")
            for key in event.keys() :
                print("\t",key," : ",event[key])



def printKeys(trace_path) :

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        # print(event.name, " : ",event.keys(),"\n")

        if re.search("net",event.name) :
            print("\n", event.name, " : ")
            if 'network_header' in event.keys() :
                print(event['network_header'])
            if 'magic' in event.keys() :
                print(event['magic'])
            if 'packet_size' in event.keys() :
                print(event['packet_size'])
            if 'skbaddr' in event.keys() :
                print(event['skbaddr'])
            if 'events_discarded' in event.keys() :
                print(event['events_discarded'])
            # print(event['content_size'])
            # print(event['v'])


    print("Fin de l'analyse")




def getEventsRegleAbsolue(trace_path):
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        regles.addRegleAbsolues(event)
        yield preprocessEventsklearn(event)



def getEventsSynthetic(trace_path):
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        yield preprocessMoreEventsklearn(event)





def afficherDictEvents(trace_path):
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        if (re.search("net_dev_",event.name)):
            print("\n", event.name, " : ")
            for key in event.keys() :
                    print("\t",key," : ",event[key])
            print("dictEvent output : ",preprocessEventsklearn(event),"\n")
            print("\n\n\n-----------------------------------------------------------------------------------------------------\n\n\n")


def main():

    trace_path = sys.argv[1]

    print(trace_path)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    getSomeEventsCSV(trace_path)

    # for event in trace_collection.events:
    #     # re.search("ioctl",event.name) or re.search("kmem",event.name) or re.search("irq",event.name)  or re.search("sched",event.name) or re.search("rcu_",event.name)
    #     if (1 ) :
            
            
    #         print("\n", event.name, " : ")
    #         for key in event.keys() :
    #                 print("\t",key," : ",event[key])
        
            

if __name__ == '__main__':
    # main()
    trace_path = sys.argv[1]

    # readAllEvents(trace_path)


    # getEventsRegleAbsolue(trace_path)
    main()

    # readAllEvents(trace_path)