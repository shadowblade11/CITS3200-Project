import speech_recognition as sr
import epitran

def getPhone(audioFile): 
    r = sr.Recognizer()
    with sr.AudioFile(audioFile) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="it-IT")
        print(text)
        epi = epitran.Epitran('ita-Latn')
        phone = epi.transliterate(text)
        print(phone)

if __name__ == "__main__" :
    source = "recording.wav"
    getPhone(source)
    submittedAudio = "recording1.wav"
    getPhone(submittedAudio)

