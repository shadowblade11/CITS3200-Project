import speech_recognition as sr
import epitran

def checkPronounciation(sourcePhone, submittedPhone):
    matchedPhone = 0 

    for x,y in zip(sourcePhone, submittedPhone): # will iterate through the list in parallel and will be limited to the shortest list
        if x == y:
            matchedPhone += 1 
    
    #finding the shortest list to calculate the score since the count is limited by the shortest list
    if len(sourcePhone) == len(submittedPhone):
        score = (matchedPhone / len(sourcePhone)) * 100 
    elif len(sourcePhone) < len(submittedPhone):
        score = (matchedPhone / len(sourcePhone)) * 100
    else:
        score = (matchedPhone / len(submittedPhone)) * 100
    
    return score

def getPhone(audioFile): 
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="it-IT") # initialisation + getting the audio to text conversion
        text = text.replace(" ", "")
        #print("%s\n"%text)
        epi = epitran.Epitran('ita-Latn') # using the package to get the phoneme string from the text
        phone = epi.transliterate(text)
        #print("%s\n"%phone)
        return phone.lower()

def convertAudio(sourceFile, submittedFile):
    source = sourceFile
    sourcePhone = getPhone(source) # converting the unicode string to IPA string (done by the package)

    submittedAudio = submittedFile 
    submittedPhone = getPhone(submittedAudio)
    score = checkPronounciation(sourcePhone, submittedPhone) # getting a score

    return score
