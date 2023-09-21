import speech_recognition as sr
from ipapy.ipastring import IPAString
import epitran

def checkPronounciation(sourcePhone, submittedPhone):
    matchedPhone = 0 

    if len(sourcePhone) >= len(submittedPhone): ## checking length so array dont go out of bounds
        longString = sourcePhone
        shortString = submittedPhone
    else:
        longString = submittedPhone
        shortString = sourcePhone
    
    for i in range(len(longString)): ## iterating through characters to find match then give a score
        if (i < len(shortString)):
            if (sourcePhone[i] == submittedPhone[i]):
                matchedPhone += 1
    
    
    score = matchedPhone / len(longString) * 100   ## score out of 100%
    return score

def getPhone(audioFile): 
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="it-IT") ## initialisation + getting the audio to text conversion
        text = text.replace(" ", "")
        #print("%s\n"%text)
        epi = epitran.Epitran('ita-Latn') ## using the package to get the phoneme string from the text
        phone = epi.transliterate(text)
        #print("%s\n"%phone)
        return phone.lower()

def convertAudio(sourceFile, submittedFile):
    source = sourceFile #change to the file you need
    sourcePhone = IPAString(unicode_string=getPhone(source)) ## converting the unicode string to IPA string (done by the package)

    submittedAudio = submittedFile #change to the file you need
    submittedPhone = IPAString(unicode_string=getPhone(submittedAudio))
    score = checkPronounciation(sourcePhone, submittedPhone) ## getting a score

    return score
