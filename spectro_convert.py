import numpy as np
import soundfile as sf
import scipy.signal as signal
import matplotlib.pyplot as plt
import csv


def norm_spec(spec):
    vects = np.array(spec)
    vects.mean(axis=1)
    return vects

# read in the metadata from the csv
audio_data = {}
bird_average = {}
with open('birdsong_metadata.csv', mode='r') as csv_file:
    birdsong_metadata = csv.DictReader(csv_file)

    line_number = 0
    bird_name = ""
    for row in birdsong_metadata:
        if line_number != 0:
            bird_name = row["english_cname"]
            temp = "songs/songs/xc" + row["file_id"] + ".flac"
            data, samplerate = sf.read(temp)
            audio_data[line_number] = {}
            audio_data[line_number]["data"] = data
            audio_data[line_number]["samplerate"] = samplerate
            audio_data[line_number]["file_id"] = row["file_id"]
            spectrum, freqs, bins, im = plt.specgram(audio_data[line_number]["data"], Fs=audio_data[line_number]["samplerate"])
            audio_data[line_number]["spectrum"] = spectrum
            audio_data[line_number]["freqs"] = freqs
            audio_data[line_number]["bins"] = bins
            audio_data[line_number]["im"] = im
            array = np.array(spectrum)
            output = array.mean(axis = 1)
            audio_data[line_number]["normalized"] = output

            # start bird_average calculation
            if bird_name != row["english_cname"] and bird_name is not "english_cname":
                bird_average[bird_name] = audio_data[line_number]["normalized"]
                bird_name = row["english_cname"]
            else:
                bird_average[bird_name] = np.mean( np.array([ bird_average[bird_name], audio_data[line_number]["normalized"] ]), axis=0 )

        line_number += 1

#vects = np.array(map(lambda data: norm_spec(data["spectrum"]), audio_data))

#vects[line_number]
    
# add axis labels
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
plt.savefig("spectrogram.png")

