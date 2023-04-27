import noisereduction as nr
import numpy as np
import math
import csv
import pickle
import os
import os.path as path
import scipy.io.wavfile as wavfile
import scipy.signal as sg
import scipy
import scipy.fftpack as fftpk
import scipy.signal as sps
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
from filters import *

class Model:
    def __init__(self, filt):
        self.model_data = {}
        self.filt = filt


    def _load_file(self, filename):
        srate, adata = wavfile.read(filename)

        #clip to 1 channel
        if adata.ndim > 1:
            adata = adata[:,0]

        #downsample to 44.1 kHz
        if srate > 44100:
            newlen = round(len(adata) * float(44100) / srate) 
            adata = sps.resample(adata, newlen)
            srate = 44100

        return self.filt(srate, adata)

    def _vectorize(self, srate, adata):
        # pad_ms = 180000 # fixed length of audio file (ms)
        # assert pad_ms > len(self.adata) Basically checking to see if file is already long enough but we're making them all longer right?
        # silence = AudioSegment.silent(duration=pad_ms-len(self.adata)+1)
        # self.adata = self.adata + silence

        #resample 

        #clip to 1 channel
        fft = abs(scipy.fft.fft(adata, n = 7938000, overwrite_x = True))
        return fft

    def load_model(self):
        name = self.__class__.__name__
        with open(path.join("./model_data", name + "-model.pkl"), "rb") as fd:
            self.model_data = pickle.load(fd)

    def save_model(self):
        name = self.__class__.__name__
        with open(path.join("./model_data", name + "-model.pkl"), "wb+") as fd:
            pickle.dump(self.model_data, fd)


    # mutate the model from here for each datapoint
    # consider this method abstract
    def _process_datapoint(self, bird_id, vector):
        pass

        
    def confusion_matrix(self, dataset):
        matrix = {}
        for bird_id, fls in dataset.items():
            for fl in fls:
                pred = self.match(fl)
                if bird_id not in matrix:
                    matrix[bird_id] = {}
                if pred not in matrix[bird_id]:
                    matrix[bird_id][pred] = 0

                matrix[bird_id][pred] += 1
        return matrix

    # dataset : Dictionary[bird_id] = [file_path]
    # this method probably doesn't need to change
    # between models
    def train(self, dataset):
        for bird_id, fls in dataset.items():
            for fl in fls:
              audio_data = self._load_file(fl)
              vector = self._vectorize(*audio_data)
              self._process_datapoint(bird_id, vector)

    # abstract, takes in audio file and returns bird id
    def match(soundfile):
        pass
    

#define here
class KMeans(Model):
    def _process_datapoint(self, bird_id, vector):
        self.model_data.setdefault(bird_id, np.zeros(len(vector)))
        self.model_data[bird_id] = np.add(self.model_data[bird_id], vector)

    def train(self, dataset):
        for bird_id, fls in dataset.items():
            for fl in fls:
                audio_data = self._load_file(fl)
                vector = self._vectorize(*audio_data)
                self._process_datapoint(bird_id, vector)

            print(self.model_data[bird_id])
            self.model_data[bird_id] /= len(fls)
            print(self.model_data[bird_id])

    def match(self, soundfile):
        audio_data = self._load_file(soundfile)
        vector = self._vectorize(*audio_data)
        prediction = "amecro"
        distance = math.inf
        for bird_id, cluster in self.model_data.items():
            dist = np.absolute(np.linalg.norm(vector - cluster))
            if dist < distance:
                prediction = bird_id
                distance = dist
        return prediction

class SVM(Model):
    def performance(self, y_true, Y_pred, metric="accuracy"):
        if metric == "accuracy":
            return accuracy_score(y_true, Y_pred)
        else:
            return confusion_matrix(y_true, Y_pred)

    def cv_performance(self, clf, X, y, k=5):
        # Put the performance of the model on each fold in the scores array
        scores = []
        # create stratified 5-fold
        s5f = StratifiedKFold(n_splits=k, shuffle = False)
        for train_index, test_index in s5f.split(X, y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            scores.append(self.performance(y_test, y_pred))
        return np.array(scores).mean()

    def select_param_linear(
        self, X, y, k=5, metric="accuracy", C_range=[], loss="hinge", penalty="l2", dual=True
    ):
        best_performance_list = []
        for C_value in C_range:
            print(C_value)
            print(" tested\n")
            # declare linear svc
            if loss == "hinge":
                clf = LinearSVC(loss = "hinge", C = C_value)
            else:
                if penalty == "l1":
                    clf = LinearSVC(penalty = "l1", dual = False, C = C_value)
                else:
                    clf = LinearSVC(C = C_value)
            # perform cv calculations
            cv_perf_list = self.cv_performance(clf, X, y, k, metric = metric)
            # add the highest to the list
            best_performance_list.append(cv_perf_list)
        best_performance_list = np.array(best_performance_list)
        # find the best performance for all C values
        index = np.where(best_performance_list == np.amax(best_performance_list))
        C_ra = np.array(C_range)
        best_C_performance = [C_ra[index[0]], np.amax(best_performance_list)]
        return best_C_performance

    def train(self, dataset):
        print("started to train\n")
        samples = []
        features = []
        for bird_id, fls in dataset.items():
            for fl in fls:
                audio_data = self._load_file(fl)
                vector = self._vectorize(*audio_data)
                samples.append(vector)
                features.append(bird_id)
        print("samples and features complete\n")
        C_range = []
        C_range.append(10**-3)
        C_range.append(10**-2)
        C_range.append(10**-1)
        C_range.append(1)
        C_range.append(10)
        C_range.append(10**2)
        C_range.append(10**3)
        output = self.select_param_linear(samples, features, C_range = C_range)
        self.model_date["model"] = LinearSVC(loss = "hinge", C = output[0])

    def match(self, soundfile):
        audio_data = self._load_file(soundfile)
        vector = self._vectorize(*audio_data)
        return self.model_date["model"].predict(vector)

class Hybrid(Model):
    pass
    

class Test(Model):

    def load_model(self):
        pass

    def train(self, dataset):
        pass

    def _process_datapoint(self, bird_id, vector):
        fft, freqs = vector
        #print(freqs)
        
    def match(self, soundfile):
        self._load_file(soundfile)
        return "amecro"

   
    

