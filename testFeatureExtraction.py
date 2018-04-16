#!/usr/bin/env python
# -*- coding :ascii -*-

import babeltraceReader as babelRead
from sklearn.feature_extraction import DictVectorizer
import sys
import numpy as np
import pandas as pd

import re

np.set_printoptions(threshold=np.nan)

from sklearn.cluster import KMeans
from sklearn import tree
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

import ssh_Tracing.listDir as listDir

import csv
import os

import itertools

import graphviz
import subprocess

from sklearn.externals import joblib

import constructionBDD
import reglesLabelisation


# TODO utiliser les pipelines de scikit learn avec la mise en cache pour optimiser le preprocessing et les fit!!!





def createCSV(directory, outputDirectory, suffixe):  

    listeDossiers = listDir.dateSort(directory)
    # listeMachines = []

    i=1
    j=0

    for dossier in listeDossiers:
        # i+=1
        # if i > 4:
        #     break
        listedict = babelRead.getSomeEventsCSV(dossier+"/kernel")
        # print(listedict)
        clesDict = set()

        for dictionnaire in listedict:
            for key in dictionnaire.keys():
                clesDict.add(key)
        with open(outputDirectory+'/dataset'+suffixe+str(j)+'.csv','w') as fichier:   # Chaque dataset correspond à un dossier, c-a-d à un snapshot
            w=csv.DictWriter(fichier,clesDict)
            w.writeheader()
            w.writerows(listedict)
        print("Ficher "+outputDirectory+'/dataset'+suffixe+str(j)+'.csv'+" généré")
        j += 1

            
def createCSVLabelisation(directory,outputDirectory):

    j=0
 
    listeCategory = []
    listeFichiers = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]

    compt = 0

    for fichier in listeFichiers:

        print(fichier)
        fichierDataset = directory+fichier
        if os.stat(fichierDataset).st_size >= 100 :
            dictEvent = fromCSVToDict(fichierDataset)
            for event in dictEvent:
                listeCategory.append(reglesLabelisation.reglesLabelisation(event))
            
            with open(outputDirectory + fichier.split(".")[0]+"_out."+fichier.split(".")[1],'w') as fichier:   # Chaque dataset correspond à un dossier, c-a-d à un snapshot
                w=csv.writer(fichier)
                w.writerow("")
                for output in listeCategory:
                    w.writerow([output])
            del listeCategory[:]    
        j += 1




def createBDD():
    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/dataset/"))
    for event in dictDataset:
        # print(dictionnaire)
        try:
            if event["filename"]:
                constructionBDD.addFilenameBDD(event)
        except KeyError:
            pass
        try:
            if event["child_comm"] and event["parent_comm"]:
                constructionBDD.addParentChildBDD(event)
        except KeyError:
                pass
        if re.search("net_dev_queue",event["a_nomEvent"]): 
            constructionBDD.addIPBDD(event)
        

def kmeans():

    vec = DictVectorizer()

    trace_path = sys.argv[1]
    
    babelRead_vectorized = vec.fit_transform(babelRead.getExecveNet(trace_path)).toarray()
    print(vec.get_feature_names())
    # print(babelRead_vectorized)

    print("\n\n\n-----------------------------------------------------------------------------------------------------\n\n\n")

    kmeans = KMeans(n_clusters=3, random_state=0).fit(babelRead_vectorized)
    # print(kmeans.labels_)
    # print(kmeans.cluster_centers_)

    # TODO utiliser sklearn.preprocessing.LableEncoder pourconvertir les données numériques (categorical label) en données numériques


    # print(babelRead.printExecveNet(trace_path))

    # print(babelRead.getEvents(trace_path))


def kmeansFromDataset():

    vec = DictVectorizer()


    babelRead_vectorized = vec.fit_transform(readCSV()[0]).toarray()
    print(vec.get_feature_names())
    # print(babelRead_vectorized)

    print("\n\n\n-----------------------------------------------------------------------------------------------------\n\n\n")

    kmeans = KMeans(n_clusters=2, random_state=0).fit(babelRead_vectorized)
    print(kmeans.labels_)
    print(kmeans.cluster_centers_)

    # kmeans.predict(vec.fit_transform().toarray())

    # TODO utiliser sklearn.preprocessing.LableEncoder pourconvertir les données numériques (categorical label) en données numériques


    # print(babelRead.printExecveNet(trace_path))

    # print(babelRead.getEvents(trace_path))





def SVMFromCSV() :
    vec = DictVectorizer(separator=':')
    nb_listes = sum(1 for i in readCSV_data())
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data())

    for item in readCSV_output():
        listeOutput = listeOutput  + item 


    # TODO Utiliser feature union pour les différents dicvctorizer correspondant à chaque fichier?


    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    print(vec.feature_names_)

    category = listeOutput

    clf = svm.SVC(decision_function_shape="ovr")
    clf.fit(babelRead_vectorized,category)


    print(clf.predict(vec.transform({"packet_size":98304, "events_discarded":0, "filename":"/bin/rm", "stream_instance_id":0, "cpu_id":0, "content_size":75624, "stream_id":0, "mode":1, "packet_seq_num":8, "a_nomEvent": "syscall_access", "magic":3254525889}).toarray()))



def RandomForestFromCSV() :
    vec = DictVectorizer(separator=':')
    nb_listes = sum(1 for i in readCSV_data())
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data())

    for item in readCSV_output():
        listeOutput = listeOutput  + item 

    # TODO Utiliser feature union pour les différents dicvctorizer correspondant à chaque fichier?

    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    print(vec.feature_names_)

    category = listeOutput

    clf = RandomForestClassifier()
    clf.fit(babelRead_vectorized,category)


    print(clf.predict(vec.transform({"packet_size":98304, "events_discarded":0, "filename":"/bin/rm", "stream_instance_id":0, "cpu_id":0, "content_size":75624, "stream_id":0, "mode":1, "packet_seq_num":8, "a_nomEvent": "syscall_entry_access", "magic":3254525889}).toarray()))



def MLPFromCSV() :
    vec = DictVectorizer(separator=':')
    nb_listes = sum(1 for i in readCSV_data())
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data())

    for item in readCSV_output():
        listeOutput = listeOutput  + item 

    # TODO Utiliser feature union pour les différents dicvctorizer correspondant à chaque fichier?

    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    print(vec.feature_names_)

    category = listeOutput

    clf = MLPClassifier(solver="lbfgs", alpha=1e-5, hidden_layer_sizes=(5,2), random_state=1)
    clf.fit(babelRead_vectorized,category)


    print(clf.predict(vec.transform({"packet_size":98304, "events_discarded":0, "filename":"/bin/rm", "stream_instance_id":0, "cpu_id":0, "content_size":75624, "stream_id":0, "mode":1, "packet_seq_num":8, "a_nomEvent": "syscall_entry_access", "magic":3254525889}).toarray()))







def OneCLassSVMPredict(modele, dictVec):
    clf = joblib.load(modele)
    vec = joblib.load(dictVec)
    print(clf.predict(vec.transform({"packet_size":98304, "events_discarded":0, "filename":"/bin/rm", "stream_instance_id":0, "cpu_id":0, "content_size":75624, "stream_id":0, "mode":1, "packet_seq_num":8, "a_nomEvent": "syscall_open", "magic":3254525889}).toarray()))






def OneClassSVMFromCSV():
    vec = DictVectorizer(separator=':')
    nb_listes = sum(1 for i in readCSV_data("./data/dataset/"))
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/dataset/"))

    for item in readCSV_output("./data/datasetOutput/"):
        listeOutput = listeOutput  + item 


    # TODO Utiliser feature union pour les différents dicvctorizer correspondant à chaque fichier?


    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    # print(vec.feature_names_)
    print("BabeltraceVectorized Ok")
    clf = svm.OneClassSVM(kernel="rbf")
    clf.fit(babelRead_vectorized)

    print("Entrainement termine")

    # TODO le Vec est le même pour tout les algos, checker s'il existe et le charger serait plus rapide que le regénérer à chaque fois?
    save = None
    save = joblib.dump(vec,"./modeles/oneClassSVMVec.p")
    save = joblib.dump(clf,"./modeles/oneClassSVM.p")
    if save != None :
        print("Enregistrement du modèle achevé!")
    else:
        print("Erreur lors de l'enregistrement")


















def DessinerArbre(clf,vec):
    listeOutput = []
    for item in readCSV_output("./data/datasetOutput/"):
        listeOutput = listeOutput  + item 

    category = [0,1]

    dot_file = open("arbre.dot","w")
    dot_data = tree.export_graphviz(clf, out_file=dot_file, feature_names=vec.feature_names_, class_names=str(category), filled=True, rounded=True)
    dot_file.close()


    command = ["dot","-Tpng","arbre.dot","-o","arbre.png"]
    try:
        subprocess.check_call(command)
    except:
        exit ("Impossible de tracer l'arbre")

def DecisionTreePredict(modele, dictVec):
    clf = joblib.load(modele)
    print("Modèle loadé")
    vec = joblib.load(dictVec)
    print(clf.predict(vec.transform({"packet_size":98304, "events_discarded":0, "filename":"/bin/rm", "stream_instance_id":0, "cpu_id":0, "content_size":75624, "stream_id":0, "mode":1, "packet_seq_num":8, "a_nomEvent": "syscall_open", "magic":3254525889}).toarray()))

    DessinerArbre(clf,vec)


def DecisionTreeFromCSV() :
    vec = DictVectorizer(separator=':')
    nb_listes = sum(1 for i in readCSV_data("./data/dataset/"))
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/dataset/"))

    for item in readCSV_output("./data/datasetOutput/"):
        listeOutput = listeOutput  + item 


    # TODO Utiliser feature union pour les différents dicvctorizer correspondant à chaque fichier?


    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    print(vec.feature_names_)

    category = listeOutput

    clf = tree.DecisionTreeClassifier()
    clf.fit(babelRead_vectorized,category)

    save = None
    save = joblib.dump(vec,"./modeles/decisionTreeVec.p")
    save = joblib.dump(clf,"./modeles/decisionTree.p")
    if save != None :
        print("Enregistrement du modèle achevé!")
    else:
        print("Erreur lors de l'enregistrement")





def fromCSVToDict(fichier):

    with open(fichier,"r") as dataset:  
        reader = csv.reader(dataset,delimiter=',')
        featureName=next(reader)
        nbFeature = len(featureName)
        my_dict={}
        # for row in reader:
        #     my_dict = {featureName[i]: row[i] for i in range (nbFeature) if row[i] is not ''}
        #     yield my_dict
        for row in reader:
            for i in range(nbFeature):
                if row[i] is not '':
                    try:
                        my_dict[featureName[i]]=int(row[i])
                    except ValueError as erreurInt:
                        my_dict[featureName[i]]= row[i]

                    # if featureName[i]=="filename" or featureName[i]=="a_nomEvent" or featureName[i]=="name"  or featureName[i]=="s" or featureName[i]=="parent_comm" or featureName[i]=="comm":
                    #     my_dict[featureName[i]]= row[i]
                    # else:
                    #     my_dict[featureName[i]]=int(row[i])
            yield my_dict
            my_dict.clear()


def outputReadCSV(fichier):

    listeOutput = []
    with open(fichier,"r") as dataset:  
        reader = csv.reader(dataset)
        next(reader)
        for row in reader:
            listeOutput.append(int(row[0]))
    return listeOutput


def readCSV_data(dossierData): # To be sure that each file is reading the data and the output at the same time

    listeFichiers = [name for name in os.listdir(dossierData) if os.path.isfile(os.path.join(dossierData, name))]
    listeFichiers.sort()
    print(len(listeFichiers))

    # TODO attention, certains CSV peuvent-être vides! Peut-être toujours écrire l'event net_dev_queue recurrent?

    for fichier in listeFichiers:
        if os.stat(dossierData + fichier).st_size >= 100 :
            yield fromCSVToDict(dossierData+fichier)


def readCSV_output(DossierDataOutput): # To be sure that each file is reading the data and the output at the same time

    indiceFichier = 0
    listeFichier = [name for name in os.listdir(DossierDataOutput) if os.path.isfile(os.path.join(DossierDataOutput, name))]
    listeFichier.sort()
    print(DossierDataOutput)
    print(listeFichier)

    # TODO attention, certains CSV peuvent-être vides!On regarde leur taille pour être certain qu'ils soient rempli. Peut-être toujours écrire l'event net_dev_queue recurrent?

    for fichier in listeFichier:
        if os.stat(DossierDataOutput+fichier).st_size >= 100 :
            yield outputReadCSV(DossierDataOutput+fichier)




def main():

    ##### To get the CSV in order to train the algo #####
    # directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/hassbian"
    # listeDirectory = createCSV(directory)


    ##### To train #####
    # kmeansFromDataset()
    # kmeans()

    # DecisionTreeFromCSV()
    # DecisionTreePredict("./modeles/decisionTree.p","./modeles/decisionTreeVec.p")

    # SVMFromCSV()

    # RandomForestFromCSV()

    # MLPFromCSV()


    # TODO s'assurer que le dataset a bien été généré avant de lancer l'entrainement
    ans = True
    while ans:
        print("""
        #######################################
        ##                                   ##
        ##  Machine learning sur les traces  ##
        ##                                   ##
        #######################################

        1. Génération CSV et BDD
        2. Générer CSV attaque
        3. Génération Labels
        4. Entrainement Arbre de décision
        5. Prediction arbre de décision
        6. Entrainement OneClassSVM
        7. Prediction SVM
        8. Quit  
         """)

        ans = input()
        if ans == "1":
            directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/hassbian"
            createCSV(directory,"./data/dataset","")
            createBDD()
        if ans == "2":
            directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/infecte/hassbian"
            createCSV(directory,"./data/dataset","Infecte")
        elif ans == "3":
            input("Le dataset a-t-il bien été généré?")
            directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/data/dataset/"
            createCSVLabelisation(directory,"./data/datasetOutput/")
            print("Génération des fichiers dataset effectuée")
        elif ans == "4":
            input("Le dataset ET les labels ont-ils bien été générés?")
            DecisionTreeFromCSV()
        elif ans == "5":
            input("Le modèle a-t-il bien été entrainé?")
            DecisionTreePredict("./modeles/decisionTree.p","./modeles/decisionTreeVec.p")
        elif ans == "6":
            input("Le dataset ET les labels ont-ils bien été générés?")
            OneClassSVMFromCSV()
        elif ans == "7":
            input("Le modèle a-t-il bien été entrainé?")
            OneCLassSVMPredict("./modeles/oneClassSVM.p","./modeles/oneClassSVMVec.p")
        elif ans == "8":
            break
        elif ans !="" :
            print("Ce choix n'est pas correct")








if __name__ == '__main__':
    main()