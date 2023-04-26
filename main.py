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
    match arguments[0]:
        case ("-m", "kmeans"):
            model = KMeans(filt)
        case ("-m", "svm"):
            model = SVM(filt)
        case ("-m", "hybrid"):
            model = Hybrid(filt)
        case ("-m", "test"):
            model = Test(filt)
        case other:
            print("invalid model, options: test, kmeans, svm, hybrid")
            sys.exit(1)
    
    match values[0]:
        case "train":
          files = get_dataset(
              "./annarborsamples",
              (~has_song) & has_call & is_bitrate(44100)
          )
          train(model, files)
        case "match":
          match(model, values[1])
        case other:
            print("unknown command ", values[0]) 

main()
# Run this line to load the data from file after you've read and processed the data once
# load_data("none")
