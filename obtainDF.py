import pandas
import allosaurus.app
import panphon

def timestampOutput(output):
    records = []
    lines = output.split('\n')
    for line in lines:
        tmp = line.split(' ')
        start = float(tmp[0])
        duration = float(tmp[1])
        end = start + duration
        label = tmp[2]
        records.append(dict(start=start, duration=duration, end=end,label=label))
    df = pandas.DataFrame.from_records(records)
    return df

def isConsonant(ipa):
    ft = panphon.FeatureTable()
    cons = ft.word_fts(ipa)[0] >= {'cons': 1}
    return cons

def recognizePhones(path, emit=1.2, lang='eng'):
    model = allosaurus.app.read_recognizer()
    out = model.recognize(path, lang, timestamp=True, emit=emit)
    
    phones = timestampOutput(out)
    phones['consonant'] = phones['label'].apply(isConsonant)
    return phones