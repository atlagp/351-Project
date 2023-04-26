import noisereduction as nr
import csv
import os.path as path

class IdFilter:
    def __init__(self, *args):
        if len(args ) > 1:
          self._filter = args[0]

    #default identity transformation
    def _filter(ad, srate):
        return (srate, adata)

    def __call__(adata, srate):
        return self._filter( srate, adata)

    #make filters composable 
    def __rshift__(self, f): 
        return IdFilter(lambda srate, adata: f(*self(srate, adata)))

class Wiener(IdFilter):
    def _filter(adata, srate):
        # write something that windows through the audio data and
        # finds the largest interval of "silence"

        noise_begin, noise_end = 0, 10 # window in second where only noise is present 
        # IDK WHAT TO PUT FOR NOISE_END BC OF VARIABLE AUDIO LENGTH :)
        # moudov/XC31137
        noised_audio = nr.Wiener(srate, adata, noise_begin, noise_end)
        return noised_audio.wiener() #simple noise reduction

