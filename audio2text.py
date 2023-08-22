import speech_recognition as sr
import eng_to_ipa as ipa

source = "recording.wav"
target = "recording1.wav"

r = sr.Recognizer()

with sr.AudioFile(source) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)
    print(ipa.convert(text))

with sr.AudioFile(target) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)
    print(ipa.convert(text))