import noisereduction as nr
import csv
import pickle
import os
import os.path as path
import scipy.io.wavfile as wavfile
import scipy.signal as sg
import scipy
import scipy.fftpack as fftpk
import scipy.signal as sps
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
            newlen = round(len(data) * float(new_rate) / sampling_rate) 
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
        print(adata)
        fft = abs(scipy.fft.fft(adata, n = 7938000, overwrite_x = True))
        freqs = fftpk.fftfreq(len(fft), (1.0/srate))
        return (fft, freqs)

    def load_model(self):
        name = self.__class__.__name__
        with open(path.join("./model_data", name + "-model.pkl", "r")) as fd:
            self.model_data = pickle.load(fd)

    def save_model(self):
        name = self.__class__.__name__
        with open(path.join("./model_data", name + "-model.pkl", "rw+")) as fd:
            pickle.load(self.model_data, fd)

    # mutate the model from here for each datapoint
    # consider this method abstract
    def _process_datapoint(self, bird_id, vector):
        pass

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
    pass

class SVM(Model):
    pass
    
class Hybrid(Model):
    pass
    

class Test(Model):

    def load_model(self):
        pass

    def _process_datapoint(self, bird_id, vector):
        fft, freqs = vector
        print(len(fft))
        #print(freqs)
        
    def match(self, soundfile):
        self._load_file(soundfile)
        return "amecro"

   
    

