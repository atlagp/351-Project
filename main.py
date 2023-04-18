import numpy as np
import soundfile as sf
import scipy.signal as signal
import matplotlib.pyplot as plt
import csv
import os

def k_means_no_filter():
    return 0

def k_means_wiener_filter():
    return 0

def read_data(filter):
    if filter == "none":
        directory = 'annarborsamples'
        
        # iterate over files in
        # that directory
        for temp in os.scandir(directory):
            bird = temp.path
            for filename in os.scandir(bird):
                if filename.is_file():
                    print(filename.path)
            return 0
        return 0
    if filter == "wiener":
        return 0
    return 0

def load_data(filter):
    if filter == "none":
        return 0
    if filter == "wiener":
        return 0
    return 0



# Begin main

# Run this line once to read in the audio data
read_data("none")

# Run this line to load the data from file after you've read and processed the data once
# load_data("none")