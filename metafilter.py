import audio_metadata as am
import os
import os.path as path

def num_items(d):
    s = 0
    for k, v in d.items():
        s += len(v)
    return s

def sanitize_comment(cmt):
    cmt.replace("/  /", "//")
    return cmt.split("//")

def get_dataset(root_dir, md_filter):
    def filter_file(fp):
        meta = am.load(fp)
        if(".wav" not in fp):
            return False
        #preprocess comment
        meta["tags"]["comment"] = sanitize_comment(meta["tags"]["comment"][0])
        return md_filter(meta)

    filtered = {}
    for basep, dname, fnames in os.walk(root_dir):
        if not fnames:
            continue
        fpaths = list(filter(
            filter_file,
            map(lambda f: path.join(basep, f), fnames)
        ))
        bird_id = path.basename(basep)
        filtered[bird_id] = fpaths
    print("] training on %i files" % num_items(filtered))
    return filtered

#filter out everything that isn't a 44.1Khz bird call recording
class MetaFilter: 
    def __init__(self, fun):
        self.__fun = fun
    def __call__(self, meta):
        return self.__fun(meta)
    def __and__(self, f2):
        return MetaFilter(lambda x: self.__fun(x) and f2.__fun(x))
    def __or__(self, f2):
        return MetaFilter(lambda x: self.__fun(x) or f2.__fun(x))
    def __invert__(self):
        return MetaFilter(lambda x: not self.__fun(x))

   
@MetaFilter
def has_call(meta):
    return ("call" in meta["tags"]["comment"][4].lower())

@MetaFilter
def has_song(meta):
    return ("song" in meta["tags"]["comment"][4].lower())

@MetaFilter
def only_call(meta):
    return "call" in meta["tags"]["comment"][4].lower().replace(",","").strip()

def bitrate(br):
    return MetaFilter(lambda meta: (meta["streaminfo"]["sample_rate"] == br))

def species_id(species_id):
    return MetaFilter(lambda meta: path.basename(path.dirname(meta["filepath"])).lower() == species_id)

def file_id(file_id):
    return MetaFilter(lambda meta: path.basename(meta["filepath"]).lower() == (file_id.lower() + ".wav"))
    
