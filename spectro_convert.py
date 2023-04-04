import numpy as np
import soundfile as sf
import scipy.signal as signal
import matplotlib.pyplot as plt

data, samplerate = sf.read("songs/songs/xc101862.flac")

Pxx, freqs, bins, im = plt.specgram(data, Fs=samplerate)

# add axis labels
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')