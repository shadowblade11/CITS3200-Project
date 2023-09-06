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
        records.append(dict(start=start, end=end, label=label))
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

##finding the ratio of vowels and consonants
def getRatio(phones):
    vowel = 0
    consonant = 0
    for x in phones['consonant'].values:
        if x == True:
            consonant += 1
        else:
            vowel += 1

    return(vowel/consonant) 

def compareRatio(submitted, source): # keep ratio within +-0.3
    if submitted == source :
        return 100
    if submitted - source <= 0.3 and submitted - source > 0:
        return 100 - (100 * (submitted - source))
    if source - submitted <= 0.3 and source - submitted > 0:
        return 100 - (100 * (source - submitted))
    elif submitted > source:
        return 100 * (submitted - source)
    else: 
        return 100 * (source - submitted)


def getCandV(sourceFile, submittedFile):
    submittedAudio = submittedFile
    submittedPhones = recognizePhones(submittedAudio)

    source = sourceFile
    sourcePhones = recognizePhones(source)
    
    score = compareRatio(getRatio(submittedPhones), getRatio(sourcePhones))
    return score 