#!/usr/bin/env python 

import numpy as np
import soundfile as sf
import csv
import os
import sys
import getopt
from filters import *
from models import *
from metafilter import *

def match(model, fl):
    model.load_model()
    print(model.match(fl))

def train(model, files):
    model.train(files)
    model.save_model()

def main():
    args = sys.argv[1:]

    options = "m:"
    long_options = ["model="]

    arguments, values = getopt.getopt(args, options, long_options)

    filt = Wiener() >> IdFilter()

    model = {}
    arg = arguments[0]
    if arg == ("-m", "kmeans"): 
        model = KMeans(filt)
    elif arg == ("-m", "svm"):
      model = SVM(filt)
    elif arg ==  ("-m", "hybrid"):
      model = Hybrid(filt)
    elif arg == ("-m", "test"):
        model = Test(filt)
    else:
        print("invalid model, options: test, kmeans, svm, hybrid")
        sys.exit(1)
        
    arg = values[0]
    if arg == "train":
        files = get_dataset(
            "./annarborsamples",
            (~has_song) & has_call & species_id("amecro")
        )
        train(model, files)
    elif arg == "match":
        match(model, values[1])
    else:
        print("unknown command ", values[0]) 

main()
# Run this line to load the data from file after you've read and processed the data once
# load_data("none")
