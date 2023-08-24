from speech_recognition import Recognizer,AudioFile


source = "../audio/pronunciation_it_buongiorno.wav"

def get_text(audio_file):
    rec = Recognizer()
    with AudioFile(audio_file) as audio_track:
        audio = rec.record(audio_track)
    
    text = rec.recognize_google(audio,language="it-IT")
    print(text)


get_text(source)