import pandas
import allosaurus.app
import panphon

def timestampOutput(output):
    records = []
    lines = output.split('\n') # parsing the output into a dataframe
    for line in lines:
        tmp = line.split(' ')
        start = float(tmp[0]) # start time of recognized phone
        duration = float(tmp[1]) # how long it was pronounced for
        end = start + duration # when pronounciation of the phone ended (timestamp)
        label = tmp[2] # the phone pronounced
        records.append(dict(start=start, duration=duration, end=end,label=label)) #adding to dict 
    df = pandas.DataFrame.from_records(records) # adding to df
    return df

def isConsonant(ipa):
    ft = panphon.FeatureTable()  #checking if the phone is a consonant or not
    cons = ft.word_fts(ipa)[0] >= {'cons': 1}
    return cons 

def recognizePhones(path, emit=1.2, lang='eng'):
    model = allosaurus.app.read_recognizer() 
    out = model.recognize(path, lang, timestamp=True, emit=emit) #receiving the output of audio file from API model
    
    phones = timestampOutput(out)
    phones['consonant'] = phones['label'].apply(isConsonant) #adding consonant feature to df
    return phones