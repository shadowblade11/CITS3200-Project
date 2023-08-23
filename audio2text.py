import speech_recognition as sr
import epitran

def checkPronounciation(sourcePhone, submittedPhone):
    matchedPhone = 0
    print(len(sourcePhone))
    print(len(submittedPhone))
    if len(sourcePhone) >= len(submittedPhone):
        longString = sourcePhone
        shortString = submittedPhone
    else:
        longString = submittedPhone
        shortString = sourcePhone
    
    for i in range(len(longString)):
        if (i < len(shortString)):
            if (sourcePhone[i] == submittedPhone[i]):
                matchedPhone += 1
    
    score = matchedPhone / len(longString)    
    print(score)

def getPhone(audioFile): 
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="it-IT")
        print(text)
        epi = epitran.Epitran('ita-Latn')
        phone = epi.transliterate(text)
        print(phone)
        return phone

if __name__ == "__main__" :
    
    source = "recording.wav"
    sourcePhone = getPhone(source)
    
    submittedAudio = "recording1.wav"
    submittedPhone = getPhone(submittedAudio)
    checkPronounciation(sourcePhone, submittedPhone)


