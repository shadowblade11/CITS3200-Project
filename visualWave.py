import pandas
import numpy
import librosa

from matplotlib import pyplot as plt
import librosa.display

import allosaurus.app
import panphon

def parse_timestamp_output(output):
    records = []
    lines = output.split('\n')
    for line in lines:
        tok = line.split(' ')
        start = float(tok[0])
        duration = float(tok[1])
        end = start + duration
        label = tok[2]
        records.append(dict(start=start, end=end, label=label))
    df = pandas.DataFrame.from_records(records)
    return df

def is_consonant(ipa):
    ft = panphon.FeatureTable()
    cons = ft.word_fts(ipa)[0] >= {'cons': 1}
    return cons

def phone_recognize_file(path, emit=1.2, lang='eng'):

    model = allosaurus.app.read_recognizer()
    out = model.recognize(path, lang, timestamp=True, emit=emit)
    
    phones = parse_timestamp_output(out)
    phones['consonant'] = phones['label'].apply(is_consonant)
    phones['color'] = phones['consonant'].replace({True: 'green', False: 'red'})
    return phones

if __name__ == '__main__':
    submittedPath = 'recording.wav'
    submittedPhones = phone_recognize_file(submittedPath)
    print(submittedPhones)
    print("\n")

    sourcePath = 'audiofiles_wav/Come_Ti_Chiami.wav'
    sourcePhones = phone_recognize_file(sourcePath)
    print(sourcePhones)

