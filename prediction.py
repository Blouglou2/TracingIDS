#!/usr/bin/env python
# -*- coding :ascii -*-

from babeltraceReader import *
from sklearn.externals import joblib

import babeltrace

import threading, queue
from datetime import datetime
import os



def DecisionTreePredict(trace_path):
    
    modele = "./modeles/decisionTree.p"
    dictVec = "./modeles/dictVec.p"
    
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    listeMachines = []
    dicTid = {}
    dictCPUid = {}

    # print(trace_path)

    tempsDebut = datetime.now().time()
    print("\tTemps debut : "+ str(tempsDebut))


    for event in trace_collection.events:
        try :
            # print("Avant preprocessing")
            eventpreprocessed = preprocessMoreEventsklearn(event,listeMachines,dicTid,dictCPUid)
            # print("Après preprocessing")
            # print(eventpreprocessed)
            # print("Avant predict")
            if clf.predict(vec.transform(eventpreprocessed).toarray()) != [0]:
                # print("Alerte Intrusion sur le système :")
                # print(eventpreprocessed)
                # print(datetime.now().time())
                # print("----------------------------------")
                pass
            # print("Après predict")
        except TypeError:
            pass
    # print("\n\nFin de traitement de la trace "+trace_path)


def RandomForestPredict(trace_path):
    
    modele = "./modeles/randomForest.p"
    dictVec = "./modeles/dictVec.p"
    
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    listeMachines = []
    dicTid = {}
    dictCPUid = {}

    # print(trace_path)

    tempsDebut = datetime.now().time()
    print("\tTemps debut : "+ str(tempsDebut))


    for event in trace_collection.events:
        try :
            # print("Avant preprocessing")
            eventpreprocessed = preprocessMoreEventsklearn(event,listeMachines,dicTid,dictCPUid)
            # print("Après preprocessing")
            # print(eventpreprocessed)
            # print("Avant predict")
            if clf.predict(vec.transform(eventpreprocessed).toarray()) != [0]:
                # print("Alerte Intrusion sur le système :")
                # print(eventpreprocessed)
                # print(datetime.now().time())
                # print("----------------------------------")
                pass
            # print("Après predict")
        except TypeError:
            pass
    # print("\n\nFin de traitement de la trace "+trace_path)


def OneClassSVMPredict(trace_path):
    
    modele = "./modeles/oneClassSVM.p"
    dictVec = "./modeles/dictOneClassVec.p"
    
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    listeMachines = []
    dicTid = {}
    dictCPUid = {}

    # print(trace_path)
    tempsDebut = datetime.now().time()
    print("\tTemps debut : "+ str(tempsDebut))

    for event in trace_collection.events:
        try :
            # print("Avant preprocessing")
            eventpreprocessed = preprocessMoreEventsklearn(event, listeMachines,dicTid,dictCPUid)
            # print("Après preprocessing")
            # print(eventpreprocessed)
            # print("Avant predict")
            if eventpreprocessed != {}:
                try:
                    if clf.predict(vec.transform(eventpreprocessed).toarray()) == [-1] :    # and eventpreprocessed["a_nomEvent"]  != "net_dev_queue"
                    #     print("Alerte Intrusion sur le système :")
                    # print(eventpreprocessed)
                    # print(datetime.now().time())
                    # print("----------------------------------")
                        pass
                    # print("Après predict")
                except KeyError:
                    pass
        except TypeError:
            pass

def MLPPredict(trace_path):
    
    modele = "./modeles/MLP.p"
    dictVec = "./modeles/dictVec.p"
    
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    listeMachines = []
    dicTid = {}
    dictCPUid = {}

    # print(trace_path)

    tempsDebut = datetime.now().time()
    print("\tTemps debut : "+ str(tempsDebut))

    for event in trace_collection.events:
        try :
            # print("Avant preprocessing")
            eventpreprocessed = preprocessMoreEventsklearn(event, listeMachines,dicTid,dictCPUid)
            # print("Après preprocessing")
            # print(eventpreprocessed)
            # print("Avant predict")
            if eventpreprocessed != {}:
                try:
                    if clf.predict(vec.transform(eventpreprocessed).toarray()) != [0]:     # and eventpreprocessed["a_nomEvent"]  != "net_dev_queue"
                        # print("Alerte Intrusion sur le système :")
                    # print(eventpreprocessed)
                    # print(datetime.now().time())
                    # print("----------------------------------")
                        pass
                    # print("Après predict")
                except KeyError:
                    pass
        except TypeError:
            pass



def GBTPredict(trace_path):
    
    modele = "./modeles/GBT.p"
    dictVec = "./modeles/dictVec.p"
    
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    listeMachines = []
    dicTid = {}
    dictCPUid = {}

    tempsDebut = datetime.now().time()
    print("\tTemps debut : "+ str(tempsDebut))

    for event in trace_collection.events:
        try :
            eventpreprocessed = preprocessMoreEventsklearn(event, listeMachines,dicTid,dictCPUid)
            if eventpreprocessed != {}:
                try:
                    if clf.predict(vec.transform(eventpreprocessed).toarray()) != [0]:   # and eventpreprocessed["a_nomEvent"]  != "net_dev_queue"
                        # print("Alerte Intrusion sur le système :")
                    # print(eventpreprocessed)
                    # print(datetime.now().time())
                    # print("----------------------------------")
                        pass
                    # print("Après predict")
                except KeyError:
                    pass
        except TypeError:
            pass

def comptEvent(trace_path):
    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')
    nbEvent = 0

    print(trace_path)
    for event in trace_collection.events:
        nbEvent += 1
    print(nbEvent)

# def enqueue(path):
#     q = queue.Queue()
#     q.put(path)


def main():
    path = "./infectedTimeBenchmark/hassbian/"

    listeDirectory = [name for name in os.listdir(path)]
    listeDirectory = [path+x+"/kernel" for x in listeDirectory]
    
    tempsDebut = ""
    tempsFin = ""

    # for directory in listeDirectory:
    #     comptEvent(directory)

    # print("Decision Tree :")
    # for directory in listeDirectory:
    #     DecisionTreePredict(directory)
    #     tempsFin = datetime.now().time()
    #     print("\tTemps fin : " + str(tempsFin) )
    
    # print("OneClass SVM :")
    # for directory in listeDirectory:
    #     OneClassSVMPredict(directory)
    #     tempsFin = datetime.now().time()
    #     print("\tTemps fin : " + str(tempsFin) )

    # print("GBT :")
    # for directory in listeDirectory:
    #     GBTPredict(directory)
    #     tempsFin = datetime.now().time()
    #     print("\tTemps fin : " + str(tempsFin) )

    # print("MLP :")
    # for directory in listeDirectory:
    #     MLPPredict(directory)
    #     tempsFin = datetime.now().time()
    #     print("\tTemps fin : " + str(tempsFin) )


    print("Random Forest :")
    for directory in listeDirectory:
        RandomForestPredict(directory)
        tempsFin = datetime.now().time()
        print("\tTemps fin : " + str(tempsFin) )





    # path = "./infecte2/hassbian/"

    # listeDirectory = [name for name in os.listdir(path)]
    # print(sorted(listeDirectory))
    # listeDirectory = [path+x+"/kernel" for x in listeDirectory]



    # for nom in listeDirectory :
    #     traceHandle = readAllEvents(nom)

    #     i = 0
    #     for event in traceHandle.events :
    #         # print(event.timestamp)
    #         print(event.name)
    #         print(event.timestamp)
    #         # print(event.items())
    #         i+=1
    #         if i > 0 :
    #             # print("\n----------------------------------\n")
    #             break
        

if __name__ == '__main__':
    main()












############### TODO : multithreader chaque observer() créer pour une détection plus rapide : faire test de la vitesse en relanceant la commande sur le terminal de droite