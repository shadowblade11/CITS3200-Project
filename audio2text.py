import speech_recognition as sr
from ipapy.ipastring import IPAString
import epitran

def checkPronounciation(sourcePhone, submittedPhone):
    matchedPhone = 0

    if len(sourcePhone) >= len(submittedPhone):
        longString = sourcePhone
        shortString = submittedPhone
    else:
        longString = submittedPhone
        shortString = sourcePhone
    
    for i in range(len(longString)):
        if (i < len(shortString) - 1):
            if (sourcePhone[i] == submittedPhone[i]) or (sourcePhone[i] == submittedPhone[i+1]) or (sourcePhone[i+1] == submittedPhone[i]):
                matchedPhone += 1
    
    score = matchedPhone / len(longString) * 100   
    print(score)

def getPhone(audioFile): 
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="it-IT")
        text = text.replace(" ", "")
        #print("%s\n"%text)
        epi = epitran.Epitran('ita-Latn')
        phone = epi.transliterate(text)
        print("%s\n"%phone)
        return phone.lower()

if __name__ == "__main__" :
    
    source = "recording.wav"
    sourcePhone = IPAString(unicode_string=getPhone(source))
    
    submittedAudio = "recording1.wav"
    submittedPhone = IPAString(unicode_string=getPhone(submittedAudio))
    
    checkPronounciation(sourcePhone, submittedPhone)


#ehh still dk how to assess