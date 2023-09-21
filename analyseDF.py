from obtainDF import recognizePhones

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

## finding duration of each audio files for comparison
def getDuration(phone):
    start = phone['start'][0]
    end = phone['end'][len(phone)-1]

    duration = end - start
    
    return duration

def compareDuration(sourcePhones, submittedPhones):
    source = getDuration(sourcePhones)
    submitted = getDuration(submittedPhones)
    
    if source == submitted:
        return 100
    elif submitted > source:
        return 100 - (100 * (submitted/source - 1))
    else:
        return 100 - (100 * (submitted/source))
    
def getScores(sourceFile, submittedFile):
    submittedPhones = recognizePhones(submittedFile)
    sourcePhones = recognizePhones(sourceFile)
    
    ratioScore = compareRatio(getRatio(submittedPhones), getRatio(sourcePhones))
    durationScore = compareDuration(sourcePhones, submittedPhones)
    return ratioScore,durationScore


