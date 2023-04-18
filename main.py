import numpy as np
import soundfile as sf
import scipy.io.wavfile as wavfile
import scipy.signal as sg
import scipy
import scipy.fftpack as fftpk
import matplotlib.pyplot as plt
import noisereduction as nr
import csv
import os
import audio-metadata as am
import os.path as path

def k_means_no_filter():
    return 0

def k_means_wiener_filter():
    
    return 0

# bird_files[bird_id] = ["path", "path2", ...]

def read_data(filter):
    bird_data = {}

    if filter == "none":
        directory = 'annarborsamples'
        
        # iterate over files in
        # that directory
        greatest = 0
        i = 0
        for temp in os.scandir(directory):
            bird = temp.path
            bird_name = temp
            for filename in os.scandir(bird):
                if filename.is_file():
                    s_rate, signal = wavfile.read(filename.path)
                    if s_rate == 44100:
                        FFT = abs(scipy.fft.fft(signal, n = 500))
                        freqs = fftpk.fftfreq(len(FFT), (1.0/s_rate))
                        plt.plot(freqs[range(len(FFT)//2)], FFT[range(len(FFT)//2)])
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Amplitude")
            plt.savefig("ortho" + str(i) + ".png")  
            plt.clf() 
            i += 1
            return 0
        return 0
    
    
    if filter == "wiener":
        noise_begin, noise_end = 0, 10 # window in second where only noise is present 
        # IDK WHAT TO PUT FOR NOISE_END BC OF VARIABLE AUDIO LENGTH :)
        # moudov/XC31137
        noised_audio = nr.Wiener("annarborsamples/blujay/XC175223", noise_begin, noise_end)
        noised_audio.wiener() #simple noise reduction
        """
        directory = 'annarborsamples'
        for temp in os.scandir(directory):
            bird = temp.path
            bird_name = temp
            for filename in os.scandir(bird):
                if filename.is_file():
                    audio = filename.path # name of wav file in current directory
                    noise_begin, noise_end = 0, 4 # window in second where only noise is present 
                    # IDK WHAT TO PUT FOR NOISE_END BC OF VARIABLE AUDIO LENGTH :)
                    noised_audio = nr.Wiener(audio, noise_begin, noise_end)
                    noised_audio.wiener() #simple noise reduction
                    # noised_audio.wiener_two_step() #Advanced noise reduction
                    # XC51410.wav
                    # XC134188
                    # XC109033
        return 0
        """
    return 0
    


def load_data(filter):
    if filter == "none":
        return 0
    if filter == "wiener":
        return 0
    return 0

def write_data(birds, filename): 
    with open(filename) as cluster_file:
        writer = csv.DictWriter(cluster_file, fieldnames = {
          "species_id",
          "cluster_center"  
        })
        writer.writeheader()
        for id, center in birds:
            writer.writerow({
                "species_id" : id,
                "culster_center" : center
            })


# Begin main

# Run this line once to read in the audio data
# write_data(read_data("none"), "bird_clusters.csv")
read_data("wiener")

# Run this line to load the data from file after you've read and processed the data once
# load_data("none")
def get_birdsong_files(root_dir, md_filter):
    def filter_file(fp):
        meta = am.load(fp)
        #preprocess comment
        return md_filter(meta)
    filtered = {}
    for basep, dname, fnames in os.walk(root_dir):
        fpaths = list(filter(
            map(lambda f: path.join(basep, f), fnames)
            fpaths
        ))
        bird_id = path.basename(basep)
        files[bird_id] = fpaths
        #map(lambda x: (x, 
    return filtered

# Begin main

# Run this line once to read in the audio data
get_birdsong_files("./annarborsamples", lambda x: x)

# Run this line to load the data from file after you've read and processed the data once
# load_data("none")
