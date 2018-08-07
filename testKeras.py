# LSTM for sequence classification in the IMDB dataset
# import numpy
# from keras.datasets import imdb
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import LSTM
# from keras.layers.embeddings import Embedding
# from keras.preprocessing import sequence

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import numpy

from babeltraceReader import *
from sklearn.externals import joblib

import babeltrace

import threading, queue
from datetime import datetime
import os

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
import numpy

from testFeatureExtraction import *
import os


# # fix random seed for reproducibility
# numpy.random.seed(7)
# # load the dataset but only keep the top n words, zero the rest
# top_words = 5000
# (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=top_words)
# # truncate and pad input sequences
# max_review_length = 500
# X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
# X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)
# # create the model
# embedding_vecor_length = 32
# model = Sequential()
# model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length))
# model.add(LSTM(100))
# model.add(Dense(1, activation='sigmoid'))
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# print(model.summary())
# model.fit(X_train, y_train, nb_epoch=3, batch_size=64)
# # Final evaluation of the model
# scores = model.evaluate(X_test, y_test, verbose=0)
# print("Accuracy: %.2f%%" % (scores[1]*100))


def create_model1():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=1242, activation='sigmoid'))
	model.add(Dense(4, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

def create_model2():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=1655, activation='sigmoid'))
	model.add(Dense(4, activation='sigmoid'))
	model.add(Dense(1, activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model


def create_model3():
	# create model
	model = Sequential()
	model.add(Dense(6, input_dim=1242, activation='sigmoid'))
	model.add(Dense(4, activation='sigmoid'))
	model.add(Dense(1, activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

def benchmarkLSTM():

    seed = 7
    numpy.random.seed(seed)
    
    os.system("source ~/Software/tensorflow/bin/activate")
    vec = DictVectorizer(separator=':')
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/LSTM/dataset/"))

    for item in readCSV_output("./data/LSTM/datasetOutput/"):
        listeOutput = listeOutput  + item 


    X = vec.fit_transform(dictDataset).toarray()
    Y = listeOutput

    scoring = ["accuracy","f1","precision","recall"]

    # evaluate using 5-fold cross validation
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)

    # create model
    print("Modèle 2 processing...")
    model2 = KerasClassifier(build_fn=create_model2, epochs=5, batch_size=5, verbose=1)

    

    scores2 = cross_validate(model2, X, Y, cv=5,scoring = scoring )
    print(scores2)

    save = joblib.dump(vec,"./modeles/dictVecLSTM.p")

    print("-----------------------------------")
    
    save = None
    save = joblib.dump(model2,"./modeles/LSTM.p")
    if save != None :
        print("Enregistrement du modèle achevé!")
    else:
        print("Erreur lors de l'enregistrement")
    # print("----------------------------------")
    # with open("benchmark.txt","a") as fichierBenchmark:
    #     fichierBenchmark.write("-------------------------------\n")
    #     fichierBenchmark.write("LSTM:\n")
    #     fichierBenchmark.write("\t Accuracy {:5.4f} (+/- {:5.4f})\n".format(scores2["test_accuracy"].mean(), scores2["test_accuracy"].std()*2))
    #     fichierBenchmark.write("\t F1 {}\n".format(scores2["test_f1"].mean()))

def LSTMFromCSV():

    seed = 7
    numpy.random.seed(seed)
    
    os.system("source ~/Software/tensorflow/bin/activate")
    vec = DictVectorizer(separator=':')
    listeOutput = []

    dictDataset = itertools.chain.from_iterable(readCSV_data("./data/LSTM/dataset/"))

    for item in readCSV_output("./data/LSTM/datasetOutput/"):
        listeOutput = listeOutput  + item 


    X = vec.fit_transform(dictDataset).toarray()
    Y = listeOutput

    # evaluate using 10-fold cross validation
    kfold = StratifiedKFold(n_splits=5, shuffle=False, random_state=seed)

    # create model
    print("Modèle 1 processing...")
    model1 = KerasClassifier(build_fn=create_model1, epochs=5, batch_size=5, verbose=1)
    # results1 = cross_val_score(model1, X, Y, cv=kfold)
    print("-----------------------------------")
    # print(results1)
    # print(results1.mean())

    save = joblib.dump(vec,"./modeles/dictVecLSTM.p")

    print("-----------------------------------")

    save = None
    save = joblib.dump(model1,"./modeles/LSTM.p")
    if save != None :
        print("Enregistrement du modèle achevé!")
    else:
        print("Erreur lors de l'enregistrement")

    # print("Modèle 1 processing...")
    # model2 = KerasClassifier(build_fn=create_model2, epochs=5, batch_size=5, verbose=0)
    # results2 = cross_val_score(model2, X, Y, cv=kfold)
    # print("-----------------------------------")
    # print(results2.mean())

    # print("Modèle 1 processing...")
    # model3 = KerasClassifier(build_fn=create_model3, epochs=5, batch_size=5, verbose=0)
    # results3 = cross_val_score(model3, X, Y, cv=kfold)
    # print("-----------------------------------")
    # print(results3.mean())




# def create_model():
#     # create model
#     model = Sequential()
#     model.add(Dense(12, input_dim=8, activation='relu'))
#     model.add(Dense(1, activation='sigmoid'))
#     # Compile model
#     model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#     return model


# def LSTMFromCSV():
#     os.system("source ~/Software/tensorflow/bin/activate")
#     vec = DictVectorizer(separator=':')
#     listeOutput = []

#     dictDataset = itertools.chain.from_iterable(readCSV_data("./data/dataset/"))

#     for item in readCSV_output("./data/datasetOutput/"):
#         listeOutput = listeOutput  + item 


#     babelRead_vectorized = vec.fit_transform(dictDataset).toarray()
#     category = listeOutput

#     # fix random seed for reproducibility
#     seed = 7
#     numpy.random.seed(seed)
#     # split into input (X) and output (Y) variables
#     X = babelRead_vectorized
#     Y = category
#     # create model
#     model = KerasClassifier(build_fn=create_model, verbose=1)
#     # define the grid search parameters
#     batch_size = [10, 20, 40, 60, 80, 100]
#     epochs = [10, 50, 100]
#     param_grid = dict(batch_size=batch_size, epochs=epochs)
#     grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1)
#     grid_result = grid.fit(X, Y)
#     # summarize results
#     print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
#     means = grid_result.cv_results_['mean_test_score']
#     stds = grid_result.cv_results_['std_test_score']
#     params = grid_result.cv_results_['params']
#     for mean, stdev, param in zip(means, stds, params):
#         print("%f (%f) with: %r" % (mean, stdev, param))



def LSTMPredict(trace_path):
    
    modele = "./modeles/LSTM.p"
    dictVec = "./modeles/dictVecLSTM.p"
    
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


def benchmarkPredictLSTM():
    path = "./infectedTimeBenchmark/hassbian/"

    listeDirectory = [name for name in os.listdir(path)]
    listeDirectory = [path+x+"/kernel" for x in listeDirectory]
    
    tempsDebut = ""
    tempsFin = ""

    print("LSTM :")
    for directory in listeDirectory:
        LSTMPredict(directory)
        tempsFin = datetime.now().time()
        print("\tTemps fin : " + str(tempsFin) )

def main():
    # os.system("source ~/Software/tensorflow/bin/activate")
    # # LSTMFromCSV()
    # benchmarkLSTM()

    benchmarkPredictLSTM()

if __name__ == '__main__':
    main()

