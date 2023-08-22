import speech_recognition as sr
import epitran as epi

source = "recording.wav"
target = "recording1.wav"

r = sr.Recognizer()

with sr.AudioFile(source) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data, language="it-IT")
    print(text)
    epitran = epi.Epitran('ita-Latn') 
    print(epitran.transliterate(text)) 


with sr.AudioFile(target) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data, language="it-IT")
    print(text)
    epitran = epi.Epitran('ita-Latn')
    print(epitran.transliterate(text))

##can use allosaurus 
# python -m allosaurus.run -i <filename>