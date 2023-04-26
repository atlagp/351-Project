import noisereduction as nr
import csv
import pickle
import os.path as path
import scipy.io.wavfile as wavfile
import scipy.signal as sg
import scipy
import scipy.fftpack as fftpk
from filters import *

class Model:
    def __init__(self, filt):
        self.model_data = {}
        self.filt = filt

    def _load_file(filename):
        return filt(*wavfile.read(filename.path))

    def _vectorize(srate, adata):
        fft = abs(scipy.fft.fft(adata, n = 500))
        freqs = fftpk.fftfreq(len(FFT), (1.0/srate))
        return (fft, freqs)

    def load_model():
        name = self.__class__.__name__
        with open(path.join("./model_data", name + "-model.pkl", "r")) as fd:
            self.model_data = pickle.load(fd)

    def save_model():
        name = self.__class__.__name__
        with open(path.join("./model_data", name + "-model.pkl", "rw+")) as fd:
            pickle.load(self.model_data, fd)

    # mutate the model from here for each datapoint
    # consider this method abstract
    def _process_datapoint(bird_id, vector):
        pass

    # dataset : Dictionary[bird_id] = file_path
    # this method probably doesn't need to change
    # between models
    def train(dataset):
        for k, v in dataset.items():
            audio_data = _load_file(v)
            vector = _vectorize(*audio_data)
            _process_datapoint(bird_id, vector)

    # abstract, takes in audio file and returns bird id
    def match(soundfile):
        pass
    

#define here
class KMeans(Model):
    pass

class SVM(Model):
    pass
    
class Hybrid(Mode):
    pass
    

   
    

