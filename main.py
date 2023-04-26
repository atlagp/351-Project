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
    print(model.match(fl))

def train(model, files):
    model.train(files)
    model.save_model()

def main():
    args = sys.argv[1:]

    options = "m:"
    long_options = ["model="]

    arguments, values = getopt.getopt(args, options, long_options)

    filt = Weiner() >> IdFilter()
    files = get_dataset(
        "./annarborsamples",
        (~has_song) & has_call & is_bitrate(44100)
    )

    model = {}
    match arguments[0]:
        case ("-m", "kmeans"):
            model = Model(filt)
        case ("-m", "svm"):
            print("foo")
        case ("-m", "hybrid"):
            print("foo")
        case other:
            print("invalid model, options: kmeans, svm, hybrid")
            sys.exit(1)
    
    match values[0]:
        case "train":
          pass
        case "match":
          pass
        case other:
            print("unknown command ", args[0]) 

main()
# Run this line to load the data from file after you've read and processed the data once
# load_data("none")
