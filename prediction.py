#!/usr/bin/env python
# -*- coding :ascii -*-

from babeltraceReader import *
from sklearn.externals import joblib

import threading, queue



def DecisionTreePredict(trace_path):
    
    modele = "./modeles/decisionTree.p"
    dictVec = "./modeles/decisionTreeVec.p"
    
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    listeMachines = []
    dicTid = {}
    dictCPUid = {}

    # print(trace_path)

    for event in trace_collection.events:
        try :
            # print("Avant preprocessing")
            eventpreprocessed = preprocessMoreEventsklearn(event,listeMachines,dicTid,dictCPUid)
            # print("Après preprocessing")
            # print(eventpreprocessed)
            # print("Avant predict")
            if clf.predict(vec.transform(eventpreprocessed).toarray()) != [0]:
                print("Alerte Intrusion sur le système :")
                print( eventpreprocessed)
                print("----------------------------------")
            # print("Après predict")
        except TypeError:
            pass
    print("Fin de traitement de la trace "+trace_path)



def OneClassSVMPredict(trace_path):
    
    modele = "./modeles/oneClassSVM.p"
    dictVec = "./modeles/oneClassSVMVec.p"
    
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)

    trace_collection = babeltrace.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    listeMachines = []
    dicTid = {}
    dictCPUid = {}

    print(trace_path)

    for event in trace_collection.events:
        try :
            # print("Avant preprocessing")
            eventpreprocessed = preprocessMoreEventsklearn(event, listeMachines,dicTid,dictCPUid)
            # print("Après preprocessing")
            # print(eventpreprocessed)
            # print("Avant predict")
            try:
                if clf.predict(vec.transform(eventpreprocessed).toarray()) == [-1] and eventpreprocessed["a_nomEvent"]  != "net_dev_queue":
                    print("Alerte Intrusion sur le système :")
                    print( eventpreprocessed)
                    print("----------------------------------")
                # print("Après predict")
            except KeyError:
                pass
        except TypeError:
            pass



# def enqueue(path):
#     q = queue.Queue()
#     q.put(path)


def main():
    # DecisionTreePredict("./hassbian")

    while True :
        print(q.get())

if __name__ == '__main__':
    main()












############### TODO : multithreader chaque observer() créer pour une détection plus rapide : faire test de la vitesse en relanceant la commande sur le terminal de droite