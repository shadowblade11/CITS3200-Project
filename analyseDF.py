from obtainDF import recognizePhones

#finding the ratio of vowels and consonants
def getRatio(df):
    vowel = 0
    consonant = 0
    for x in df['consonant'].values:
        if x == True:
            consonant += 1
        else:
            vowel += 1

    return(vowel/consonant) 

def compareRatio(sourceDF, submittedDF): # keep ratio within +-0.05 (lower is more sensitive)
    source = getRatio(sourceDF)
    submitted = getRatio(submittedDF)

    if submitted == source : # if ratio is equal then full marks
        score = 100
        return score
    elif submitted > source: # if the ratio in submitted audio is more 
        if submitted - source < 0.05: # if kept within this threshold then we will count it as perfect
            score = 100
            return score
        else:
            diff = submitted - source - 0.05
            scoreToSubtract = 100 * diff
            score = 100 - scoreToSubtract

            return score
    else:
        if source - submitted < 0.05: # if kept within this threshold then we will count it as perfect
            score = 100
            return score   
        else:
            diff = source - submitted - 0.05
            scoreToSubtract = 100 * diff
            score = 100 - scoreToSubtract

            return score


# finding duration of each audio files for comparison
def getDuration(df):
    start = df['start'][0]
    end = df['end'][len(df)-1]
    duration = end - start
    
    return duration

def compareDuration(sourceDF, submittedDF):
    source = getDuration(sourceDF)
    submitted = getDuration(submittedDF)
    
    if source == submitted: # if duration is the same then full marks
        score = 100
        return score
    
    elif submitted > source: # if submitted duration is more than source then marks will be subtracted based on how much longer it is
        diff = submitted/source - 1
        scoreToSubtract = 100 * diff
        score = 100 - scoreToSubtract
        
        return score
    
    else: # if submitted duration is less than source then marks will be subtracted based on how much shorter it is
        diff = 1 - submitted/source
        scoreToSubtract = 100 * diff
        score = 100 - scoreToSubtract
    
        return score
    
def getScores(sourceFile, submittedFile):
    submittedDF = recognizePhones(submittedFile)
    sourceDF = recognizePhones(sourceFile)
    
    ratioScore = compareRatio(sourceDF, submittedDF)
    durationScore = compareDuration(sourceDF, submittedDF)
    
    return ratioScore,durationScore


