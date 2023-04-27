import noisereduction as nr
import csv
import os.path as path
import numpy as np
import scipy
import scipy.signal as sps

class IdFilter:
    def __init__(self, *args):
        if len(args ) > 1:
          self._filter = args[0]

    #default transformation is identity 
    def _filter(self, srate, adata):
        return (srate, adata)

    def __call__(self, srate, adata):
        return self._filter( srate, adata)

    #make filters composable 
    def __rshift__(self, f): 
        return IdFilter(lambda srate, adata: f(*self(srate, adata)))

#more or less just instantaneous power
class Envelope(IdFilter):
    def _filter(self, srate, adata):
        adata = np.real(sps.hilbert(adata))
        print("envelope")
        adata
        return (srate, adata)

#essentially just a lowpass filter when downsampling
class Resample(IdFilter):
    def __init__(self, srate):
        self.newsrate = srate

    def _filter(self, srate, adata):
        #downsample to 44.1 kHz
        newlen = round(len(adata) * float(self.newsrate) / srate) 
        adata = sps.resample(adata, newlen)
        return (self.newsrate, adata)

class Wiener(IdFilter):
    def _find_changes(self, adata, start, end):
        up = np.zeros(end - start)
        down = np.zeros(end - start)
        upc = 0
        downc = 0

        if adata[start] > 0:
            up[upc]=start
            upc += 1
        else:
            down[downc]=start
            downc += 1

        last = adata[start]
        for val in adata:
            if last == 0 and val != last:
                up[upc] = val
                upc += 1
            elif val == 0 and val != last:
                downc[upc] = val
                downc += 1
            last = val

        pair = []
        upti = 0
        for dt in down[:(downc - 1)]:
            last_upt = 0
            if dt > last_upt or upti == upc:
                break
            for upt in up[upti:(upc - 1)]:
                upti += 1
                if upt > dt:
                    pair.append((dt, upt))
                    last_upt = upt
                    break

    def _peaks(self, srate, adata):
        srate, adata = (Resample(8000) >> Envelope())(srate, adata)
        threshold = np.percentile(adata, 80)

        adata[adata < threshold]
    
        impulses = self._find_changes(adata, 0, len(adata))
        return impulses

    def _filter(adata, srate):
        # write something that windows through the audio data and
        # finds the largest interval of "silence"

        noise_begin, noise_end = 0, 10 # window in second where only noise is present 
        # IDK WHAT TO PUT FOR NOISE_END BC OF VARIABLE AUDIO LENGTH :)
        # moudov/XC31137
        noised_audio = nr.Wiener(srate, adata, noise_begin, noise_end)
        return noised_audio.wiener() #simple noise reduction

