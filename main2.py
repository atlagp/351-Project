import numpy as np
import soundfile as sf
import scipy.signal as signal
import matplotlib.pyplot as plt
import csv
import os
import audio-metadata as am
import os.path as path

def k_means_no_filter():
    return 0

def k_means_wiener_filter():
    return 0


def get_birdsong_files(root_dir, md_filter):
    def filter_file(fp):
        meta = am.load(fp)
        meta["tags"]
        #md_filter()


    for basep, dname, fnames in os.walk(root_dir):
        fpaths = list(filter(
            map(lambda f: path.join(basep, f), fnames)
        ))
        bird_id = path.basename(basep)
        metadata = 
        #map(lambda x: (x, 

        
def load_data(filter):
    if filter == "none":
        return 0
    if filter == "wiener":
        return 0
    return 0


# Begin main

# Run this line once to read in the audio data
get_birdsong_files("./annarborsamples", lambda x: x)

# Run this line to load the data from file after you've read and processed the data once
# load_data("none")
