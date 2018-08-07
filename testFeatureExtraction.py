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
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.utils import shuffle
from sklearn import metrics


from itertools import tee

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

    label = 9

    for fichier in listeFichiers:

        print(fichier)

        fichierDataset = directory+fichier
        if os.stat(fichierDataset).st_size >= 100 :
            if "Infecte" not in fichier:
                
                dictEvent = fromCSVToDict(fichierDataset)
                for event in dictEvent:
                    label = reglesLabelisation.reglesLabelisation(event)
                    listeCategory.append(reglesLabelisation.reglesLabelisation(event))
                
                with open(outputDirectory + fichier.split(".")[0]+"_out."+fichier.split(".")[1],'w') as fichier:   # Chaque dataset correspond à un dossier, c-a-d à un snapshot
                    w=csv.writer(fichier)
                    w.writerow("")
                    for output in listeCategory:
                        w.writerow([output])
                del listeCategory[:]    

            else:

                dictEvent = fromCSVToDict(fichierDataset)
                listedico = []

                clesDict = set()

                for event in dictEvent:
                    label = reglesLabelisation.reglesLabelisation(event)
                    if label == 1:
                        eventCopy = event.copy()
                        listedico.append(eventCopy)
                        listeCategory.append(label)
                        # print(listedict)
                    # print(listedico)
                    # print("-------------------")
                # print(listedico)
                # print("aaaaaaaaaaaaaaaaaaaaaaaaaa")

                with open(outputDirectory + fichier.split(".")[0]+"_out."+fichier.split(".")[1],'w') as fichieroutput:   # Chaque dataset correspond à un dossier, c-a-d à un snapshot
                    w=csv.writer(fichieroutput)
                    w.writerow("")
                    for output in listeCategory:
                        w.writerow([output])

                # print(listedict)

                listedictCle = listedico[:]
                for dictionnaire in listedictCle:
                    for key in dictionnaire.keys():
                        clesDict.add(key)
                # print(listedict)



                with open(directory+"New"+fichier,"w") as fichierInputNew:
                    w2=csv.DictWriter(fichierInputNew,clesDict)
                    w2.writeheader()
                    w2.writerows(listedico)
                print("Fichier "+fichier+"New généré")

                del listedico[:]
                del listeCategory[:]    
        j += 1
    os.system("mv ./data/dataset/datasetInfecte* ./data/datasetInfecteOLD")
    os.system("./removePrefixe.sh New")
    

def createCSVLabelisationLSTM(directory,outputDirectory):

    j=0
 
    listeCategory = []
    listeFichiers = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]

    compt = 0

    label = 9

    for fichier in listeFichiers:

        print(fichier)

        fichierDataset = directory+fichier
        if os.stat(fichierDataset).st_size >= 100 :
            dictEvent = fromCSVToDict(fichierDataset)
            for event in dictEvent:
                label = reglesLabelisation.reglesLabelisation(event)
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
            if event["pathname"]:
                constructionBDD.addPathnameBDD(event)
        except KeyError:
            pass
        try:
            if event["child_comm"] and event["parent_comm"]:
                constructionBDD.addParentChildBDD(event)
        except KeyError:
                pass
        if "net_dev_queue" in event["a_nomEvent"]: 
            constructionBDD.addIPBDD(event)
        if "syscall" in event["a_nomEvent"]: 
            constructionBDD.addSyscallBDD(event)

        

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
    # nb_listes = sum(1 for i in readCSV_data("./data/dataset/"))
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_dataGoodBehavior("./data/dataset/"))

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
    save = joblib.dump(vec,"./modeles/dictOneClassVec.p")
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


    command = ["dot","-Tpng","-Gsize=40,60\!","-Gdpi=100","arbre.dot","-o","arbre.png"]
    try:
        subprocess.check_call(command)
    except:
        exit ("Impossible de tracer l'arbre")

def DecisionTreePredict(modele, dictVec):
    clf = joblib.load(modele)
    print("Modèle loadé")
    vec = joblib.load(dictVec)
    print(clf.predict(vec.transform({"packet_size":98304, "events_discarded":0, "filename":"/bin/mv", "stream_instance_id":0, "cpu_id":0, "content_size":75624, "stream_id":0, "mode":1, "packet_seq_num":8, "a_nomEvent": "syscall_open", "magic":3254525889}).toarray()))

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

    babelRead_vectorized_train,babelRead_vectorized_test, category_train, category_test = train_test_split(babelRead_vectorized,category, test_size=0.33, random_state = 42)

    clf = tree.DecisionTreeClassifier()
    # clf.fit(babelRead_vectorized,category)
    clf.fit(babelRead_vectorized_train,category_train)
    print("Score de l'arbre :")
    print(clf.score(babelRead_vectorized_test,category_test))

    save = None
    save = joblib.dump(vec,"./modeles/dictVec.p")
    save = joblib.dump(clf,"./modeles/decisionTree.p")
    if save != None :
        print("Enregistrement du modèle achevé!")
    else:
        print("Erreur lors de l'enregistrement")

















def GBTPredict(modele, dictVec):
    clf = joblib.load(modele)
    print("Modèle loadé")
    vec = joblib.load(dictVec)
    print(clf.predict(vec.transform({"packet_size":98304, "events_discarded":0, "filename":"/bin/mv", "stream_instance_id":0, "cpu_id":0, "content_size":75624, "stream_id":0, "mode":1, "packet_seq_num":8, "a_nomEvent": "syscall_open", "magic":3254525889}).toarray()))



def GBTFromCSV() :
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

    babelRead_vectorized_train,babelRead_vectorized_test, category_train, category_test = train_test_split(babelRead_vectorized,category, test_size=0.33, random_state = 42)

    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
    # clf.fit(babelRead_vectorized,category)
    clf.fit(babelRead_vectorized_train,category_train)
    print("Score du GBT :")
    print(clf.score(babelRead_vectorized_test,category_test))

    save = None
    save = joblib.dump(vec,"./modeles/dictVec.p")
    save = joblib.dump(clf,"./modeles/GBT.p")
    if save != None :
        print("Enregistrement du modèle achevé!")
    else:
        print("Erreur lors de l'enregistrement")


# TODO Fonction qui clean les CSV infecté des valeurs 0 : relire les csv et en réécrire des nouveaux avec juste les 0. Puis tenter les techniques du site. Générer d'autres traces d'infection avec des filename 
# autres de hassbian et les adresses IP dispo!



# def cleanDatasetInfecte(directoryDataset, directoryOutputDataset, directoryDatasetOutput, directoryOutputDataset):
#     # nb_listes = sum(1 for i in readCSV_data(directoryDataset))
#     listeFichiersDataset = [name for name in os.listdir(directoryDataset) if os.path.isfile(os.path.join(directoryDataset, name))]
#     listeFichiersDatasetOutput = [name for name in os.listdir(directoryDatasetOutput) if os.path.isfile(os.path.join(directoryDatasetOutput, name))]

#     for fichier in listeFichiersDataset:
#         if "Infecte" in fichier:
#             dictDataset = fromCSVToDict(fichier)

#         else :
#             os.system("mv "+directoryDataset+fichier+" "+directoryDatasetOutput+fichier)




def comptDataset(directory):
    listeFichiers = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]

    compt0 = 0
    compt1 = 0

    for fichier in listeFichiers:
        # print(directory+fichier)
        label = outputReadCSV(directory+fichier)
        for element in label:
            if element == 0:
                compt0 += 1
            elif element == 1 :
                compt1 += 1

    print("Le dataset contient {} labels 0 et {} labels 1".format(compt0,compt1))


def comptDatasetInput(directory):
    listeFichiers = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]

    dictEventStats={}

    for fichier in listeFichiers:
        # print(directory+fichier)
        dictInput = fromCSVToDict(directory+fichier)
        for element in dictInput:
            try:
                dictEventStats[element["a_nomEvent"]] +=1
            except:
                dictEventStats[element["a_nomEvent"]] = 1

    print("Le dataset contient :")
    print(dictEventStats)

    nbSyscall = 0
    for cle,val in dictEventStats.items():
        if "syscall" in cle:
            nbSyscall += val
    print("Nombre de syscall:")
    print(nbSyscall)


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

    # i = 0
    for fichier in listeFichiers:
        if os.stat(dossierData + fichier).st_size >= 5 :
            yield fromCSVToDict(dossierData+fichier)
        #     i+=1
        # if i > 20:
        #     break



def readCSV_dataGoodBehavior(dossierData): # To be sure that each file is reading the data and the output at the same time

    listeFichiers = [name for name in os.listdir(dossierData) if os.path.isfile(os.path.join(dossierData, name)) and "Infecte" not in name]
    listeFichiers.sort()
    print(len(listeFichiers))

    # TODO attention, certains CSV peuvent-être vides! Peut-être toujours écrire l'event net_dev_queue recurrent?

    # i = 0
    for fichier in listeFichiers:
        if os.stat(dossierData + fichier).st_size >= 5 :
            yield fromCSVToDict(dossierData+fichier)
        #     i+=1
        # if i > 20:
        #     break


def readCSV_Infecte(): # To be sure that each file is reading the data and the output at the same time

    dossierData = "./data/dataset/"
    DossierDataOutput = "./data/datasetOutput/"
    listeFichiers = [name for name in os.listdir(dossierData) if os.path.isfile(os.path.join(dossierData, name)) ] # and "Infecte" in name
    listeFichiers.sort()
    # print(len(listeFichiers))

    # TODO attention, certains CSV peuvent-être vides! Peut-être toujours écrire l'event net_dev_queue recurrent?

    # i = 0
    for fichier in listeFichiers:
        if os.stat(dossierData + fichier).st_size >= 5 :
            yield fromCSVToDict(dossierData+fichier),outputReadCSV(DossierDataOutput+fichier.split(".csv")[0]+"_out.csv")
        #     i+=1
        # if i > 20:
        #     break

def readCSV_output(DossierDataOutput): # To be sure that each file is reading the data and the output at the same time

    indiceFichier = 0
    listeFichier = [name for name in os.listdir(DossierDataOutput) if os.path.isfile(os.path.join(DossierDataOutput, name))]
    listeFichier.sort()
    print(DossierDataOutput)
    print(listeFichier)

    # TODO attention, certains CSV peuvent-être vides!On regarde leur taille pour être certain qu'ils soient rempli. Peut-être toujours écrire l'event net_dev_queue recurrent?

    for fichier in listeFichier:
        if os.stat(DossierDataOutput+fichier).st_size >= 5 :
            yield outputReadCSV(DossierDataOutput+fichier)




def benchmarkOneClassSVM(modele, dictVec):
    clf = joblib.load(modele)
    print("Modèle loadé")
    vec = joblib.load(dictVec)
    bonnePredict0 = 0
    bonnePredict1 = 0
    mauvaisePredict0 = 0
    mauvaisePredict1 = 0
    autre = 0
    j = 0
    for (dictionnaire,output) in readCSV_Infecte() :
        prediction = clf.predict(vec.transform(dictionnaire).toarray())
        if len(prediction) != len(output):
            print("Erreur du nombre de prediction")
            break
        for i in range(0,len(prediction)):
            if prediction[i] == +1 and output[i] == 0:
                bonnePredict0 += 1
            elif prediction[i] == +1 and output[i] == 1:
                mauvaisePredict0 +=1
            elif prediction[i] == -1 and output[i] == 0:
                mauvaisePredict1 += 1
            elif prediction[i] == -1 and output[i] == 1:
                bonnePredict1 +=1
            else :
                autre += 1
        print("dataset"+str(j)+" traite")
        j +=1
        
    print("Bonne Predict 0 : " + str(bonnePredict0))
    print("Bonne Predict 1 : " + str(bonnePredict1))
    print("Mauvaise Predict 0 : " + str(mauvaisePredict0))
    print("Mauvaise Predict 1 : " + str(mauvaisePredict1))
    print("Autre : " + str(autre))
    
    









def Benchmark():

    vec = DictVectorizer(separator=':')
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/dataset/"))

    for item in readCSV_output("./data/datasetOutput/"):
        listeOutput = listeOutput  + item 


    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    # print(vec.feature_names_)

    category = listeOutput
    

    ##################### SVM ###########################""
    vec2 = DictVectorizer(separator=':')

    dictDataset2 = itertools.chain.from_iterable(readCSV_dataGoodBehavior("./data/dataset/"))


    # TODO Utiliser feature union pour les différents dicvctorizer correspondant à chaque fichier?


    babelRead_vectorized2 = vec2.fit_transform(dictDataset2).toarray()
    
    scoring = ["accuracy","f1","precision","recall","average_precision"]


    clf1 = tree.DecisionTreeClassifier(class_weight ='balanced', criterion='gini', max_features='auto')
    clf2 = GradientBoostingClassifier(n_estimators = 50000, learning_rate = 0.1)
    clf3 = svm.OneClassSVM(kernel="rbf")    # TODO On ne peut pas faire de cross val puisque ce n'est pas supervisé
    clf4 = MLPClassifier(hidden_layer_sizes= (10, 2), solver = 'lbfgs', alpha= 0.0001)
    clf5 = svm.SVC(decision_function_shape="ovr")
    clf6 = svm.SVC(decision_function_shape="ovo")
    clf7 = RandomForestClassifier()

    # On sufle le dataset
    X,Y = shuffle(babelRead_vectorized,category)


    # scores1 = cross_validate(clf1, babelRead_vectorized, category, cv=5,scoring = scoring, n_jobs=-1 )
    # scores1 = cross_validate(clf1, X,Y, cv=5,scoring = scoring )
    # print(scores1)
    # print("----------------------------------")
    # with open("benchmark.txt","a") as fichierBenchmark:
    #     fichierBenchmark.write("----------------------------------\n")
    #     fichierBenchmark.write("Arbre de décision:\n")
    #     fichierBenchmark.write("\t Score :  {}\n".format(scores1))
    #     fichierBenchmark.write("\t Accuracy {:5.4f} (+/- {:5.4f})\n".format(scores1["test_accuracy"].mean(), scores1["test_accuracy"].std()*2))
    #     fichierBenchmark.write("\t F1 {}\n".format(scores1["test_f1"].mean()))
    #     fichierBenchmark.write("\t Precision and recall :  {}, {}\n".format(scores1["test_precision"].mean(),scores1["test_recall"].mean()))
    #     fichierBenchmark.write("\t Average precision :  {},\n".format(scores1["test_average_precision"].mean()))

    # scores2 = cross_validate(clf2, X,Y, cv=5,scoring = scoring)
    # print(scores2)
    # print("----------------------------------")
    # with open("benchmark.txt","a") as fichierBenchmark:
    #     fichierBenchmark.write("GBT:\n")
    #     fichierBenchmark.write("\t Score :  {}\n".format(scores2))
    #     fichierBenchmark.write("\t Accuracy {:5.4f} (+/- {:5.4f})\n".format(scores2["test_accuracy"].mean(), scores2["test_accuracy"].std()*2))
    #     fichierBenchmark.write("\t F1 {}\n".format(scores2["test_f1"].mean()))
    #     fichierBenchmark.write("\t Precision and recall :  {}, {}\n".format(scores2["test_precision"].mean(),scores2["test_recall"].mean()))
    #     fichierBenchmark.write("\t Average precision :  {},\n".format(scores2["test_average_precision"].mean()))

    # # # scores3 = cross_validate(clf3, babelRead_vectorized2, cv=5,scoring = scoring)
    # # # print(scores3)
    # scores4 = cross_validate(clf4, babelRead_vectorized, category, cv=5,scoring = scoring )
    # print(scores4)
    # print("----------------------------------")
    # with open("benchmark.txt","a") as fichierBenchmark:
    #     fichierBenchmark.write("MLP:\n")
    #     fichierBenchmark.write("\t Score :  {}\n".format(scores4))
    #     fichierBenchmark.write("\t Accuracy {:5.4f} (+/- {:5.4f})\n".format(scores4["test_accuracy"].mean(), scores4["test_accuracy"].std()*2))
    #     fichierBenchmark.write("\t F1 {}\n".format(scores4["test_f1"].mean()))
    #     fichierBenchmark.write("\t Precision and recall :  {}, {}\n".format(scores4["test_precision"].mean(),scores4["test_recall"].mean()))
    #     fichierBenchmark.write("\t Average precision :  {},\n".format(scores4["test_average_precision"].mean()))

    # scores5 = cross_validate(clf5, babelRead_vectorized, category, cv=5,scoring = scoring)
    # print(scores5)
    # print("----------------------------------")
    # with open("benchmark.txt","a") as fichierBenchmark:
    #     fichierBenchmark.write("SVM SVC:\n")
    #     fichierBenchmark.write("\t Score :  {}\n".format(scores5))
    #     fichierBenchmark.write("\t Accuracy {:5.4f} (+/- {:5.4f})\n".format(scores5["test_accuracy"].mean(), scores5["test_accuracy"].std()*2))
    #     fichierBenchmark.write("\t F1 {}\n".format(scores2["test_f1"].mean()))
    #     fichierBenchmark.write("\t Precision and recall :  {}, {}\n".format(scores5["test_precision"].mean(),scores5["test_recall"].mean()))
    #     fichierBenchmark.write("\t Average precision :  {},\n".format(scores5["test_average_precision"].mean()))

    # scores6 = cross_validate(clf6, babelRead_vectorized, category, cv=5,scoring = scoring )
    # print(scores6)
    # print("----------------------------------")
    # with open("benchmark.txt","a") as fichierBenchmark:
    #     fichierBenchmark.write("SVM SVC2:\n")
    #     fichierBenchmark.write("\t Score :  {}\n".format(scores6))
    #     fichierBenchmark.write("\t Accuracy {:5.4f} (+/- {:5.4f})\n".format(scores6["test_accuracy"].mean(), scores6["test_accuracy"].std()*2))
    #     fichierBenchmark.write("\t F1 {}\n".format(scores6["test_f1"].mean()))
    #     fichierBenchmark.write("\t Precision and recall :  {}, {}\n".format(scores6["test_precision"].mean(),scores6["test_recall"].mean()))
    #     fichierBenchmark.write("\t Average precision :  {},\n".format(scores6["test_average_precision"].mean()))

    scores7 = cross_validate(clf7, X,Y, cv=5,scoring = scoring )
    print(scores7)
    print("----------------------------------")
    with open("benchmark.txt","a") as fichierBenchmark:
        fichierBenchmark.write("----------------------------------\n")
        fichierBenchmark.write("Random Forest:\n")
        fichierBenchmark.write("\t Score :  {}\n".format(scores7))
        fichierBenchmark.write("\t Accuracy {:5.4f} (+/- {:5.4f})\n".format(scores7["test_accuracy"].mean(), scores7["test_accuracy"].std()*2))
        fichierBenchmark.write("\t F1 {}\n".format(scores7["test_f1"].mean()))
        fichierBenchmark.write("\t Precision and recall :  {}, {}\n".format(scores7["test_precision"].mean(),scores7["test_recall"].mean()))
        fichierBenchmark.write("\t Average precision :  {},\n".format(scores7["test_average_precision"].mean()))


def trainFromCSV():

    vec = DictVectorizer(separator=':')
    nb_listes = sum(1 for i in readCSV_data("./data/dataset/"))
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/dataset/"))

    for item in readCSV_output("./data/datasetOutput/"):
        listeOutput = listeOutput  + item 


    # TODO Utiliser feature union pour les différents dicvctorizer correspondant à chaque fichier?


    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    # print(vec.feature_names_)

    category = listeOutput

    babelRead_vectorized_train,babelRead_vectorized_test, category_train, category_test = train_test_split(babelRead_vectorized,category, test_size=0.33, random_state = 42)

    clf1 = tree.DecisionTreeClassifier(class_weight ='balanced', criterion='gini', max_features='auto')
    clf2 = GradientBoostingClassifier(n_estimators = 50000, learning_rate = 0.1)
    clf4 = MLPClassifier(hidden_layer_sizes= (10, 2), solver = 'lbfgs', alpha= 0.0001)


    # clf.fit(babelRead_vectorized,category)
    clf1.fit(babelRead_vectorized_train,category_train)

    save = None
    save = joblib.dump(vec,"./modeles/dictVec.p")

    save = joblib.dump(clf1,"./modeles/decisionTree.p")
    if save != None :
        print("Enregistrement du modèle achevé!")
    else:
        print("Erreur lors de l'enregistrement")

    clf2.fit(babelRead_vectorized_train,category_train)
    save = joblib.dump(clf2,"./modeles/GBT.p")
    if save != None :
        print("Enregistrement du modèle 2 achevé!")
    else:
        print("Erreur lors de l'enregistrement 2")


    clf4.fit(babelRead_vectorized_train,category_train)
    save = joblib.dump(clf4,"./modeles/MLP.p")
    if save != None :
        print("Enregistrement du modèle 3 achevé!")
    else:
        print("Erreur lors de l'enregistrement 3")


    clf5 = RandomForestClassifier()

    clf5.fit(babelRead_vectorized_train,category_train)

    save = None
    save = joblib.dump(clf5,"./modeles/randomForest.p")
    if save != None :
        print("Enregistrement du modèle 5 achevé!")
    else:
        print("Erreur lors de l'enregistrement 5")


def OptimisationHyperparametres():

    vec = DictVectorizer(separator=':')
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/dataset/"))

    for item in readCSV_output("./data/datasetOutput/"):
        listeOutput = listeOutput  + item 


    babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
    category = listeOutput

    babelRead_vectorized_train,babelRead_vectorized_test, category_train, category_test = train_test_split(babelRead_vectorized,category, test_size=0.33, random_state = 42)

    
        
    scoring = "f1"

    # clf1 = GridSearchCV(tree.DecisionTreeClassifier(), {"criterion":["gini","entropy"], "max_features":["auto"],"class_weight":[{0:0.4,1:0.6},"balanced"]}, scoring=scoring)
    # clf1.fit(babelRead_vectorized_train,category_train)
    # print(clf1.best_params_)
    with open("optimisation.txt","a") as fichierBenchmark:
        fichierBenchmark.write("\n\n-------------------------------------------\n")
    #     fichierBenchmark.write("Arbre de décision:\n")
    #     fichierBenchmark.write("\t Meilleur hyperparamètre : {} \n".format(clf1.best_params_))


    clf2 = GridSearchCV(GradientBoostingClassifier(),{"n_estimators" : [50000,60000], "learning_rate" : [0.1,0.01]},scoring = scoring)
    clf2.fit(babelRead_vectorized_train,category_train)
    print(clf2.best_params_)
    with open("optimisation.txt","a") as fichierBenchmark:
        fichierBenchmark.write("GBT:\n")
        fichierBenchmark.write("\t Meilleur hyperparamètres : {} \n".format(clf2.best_params_))


    clf4 = GridSearchCV(MLPClassifier(),{"solver" : ["lbfgs"], "alpha": [1e-3, 1e-4,1e-5], "hidden_layer_sizes" : [(10,2),(11,2),(9,2)]},scoring=scoring)
    clf4.fit(babelRead_vectorized_train,category_train)
    print(clf4.best_params_)
    with open("optimisation.txt","a") as fichierBenchmark:
        fichierBenchmark.write("MLP:\n")
        fichierBenchmark.write("\t Meilleur hyperparamètres : {} \n".format(clf4.best_params_))
    









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
        8. Entrainement GBT
        9. Prediction GBT
        10. Compter dataset
        11. Benchmark
        12. Générer Labels LSTM  
        13. Train modèles
        14. Quit 
        15. Benchmark OneClassSVM
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
            comptDataset("./data/datasetOutput/")
        elif ans == "4":
            input("Le dataset ET les labels ont-ils bien été générés?")
            DecisionTreeFromCSV()
        elif ans == "5":
            input("Le modèle a-t-il bien été entrainé?")
            DecisionTreePredict("./modeles/decisionTree.p","./modeles/dictVec.p")
        elif ans == "6":
            input("Le dataset ET les labels ont-ils bien été générés?")
            OneClassSVMFromCSV()
        elif ans == "7":
            input("Le modèle a-t-il bien été entrainé?")
            OneCLassSVMPredict("./modeles/oneClassSVM.p","./modeles/dictOneClassVec.p")
        elif ans == "8":
            input("Le dataset ET les labels ont-ils bien été générés?")
            GBTFromCSV()
        elif ans == "9":
            input("Le modèle a-t-il bien été entrainé?")
            GBTPredict("./modeles/GBT.p","./modeles/dictVec.p")
        elif ans == "10":
            comptDataset("./data/datasetOutput/")
            comptDatasetInput("./data/dataset/")
        elif ans == "11":
            Benchmark()
        elif ans == "12":
            # input("Le dataset a-t-il bien été généré?")
            # directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/hassbian"
            # createCSV(directory,"./data/LSTM/dataset","")
            # print("Le dataset LSTM sain a bien ete genere")

            # directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/infecte/hassbian"
            # createCSV(directory,"./data/LSTM/dataset","Infecte")

            # print("Le dataset LSTM infecte a bien ete genere")

            directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/data/LSTM/dataset/"
            createCSVLabelisationLSTM(directory,"./data/LSTM/datasetOutput/")
            print("Génération des fichiers dataset effectuée")

        elif ans == "13":
            input("Le dataset ET les labels ont-ils bien été générés?")
            trainFromCSV()
        elif ans == "14":
            break
        elif ans == "15":
                benchmarkOneClassSVM("./modeles/oneClassSVM.p","./modeles/dictOneClassVec.p")
        elif ans !="" :
            print("Ce choix n'est pas correct")








if __name__ == '__main__':
    main()