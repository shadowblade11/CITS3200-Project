# from speech_recognition import Recognizer,AudioFile
import wave
import matplotlib.pyplot as plt
import numpy as np


source = "../audio/pronunciation_it_buongiorno.wav"
source2 = "../audio/sound.wav"


# def get_text(audio_file):
#     rec = Recognizer()
#     with AudioFile(audio_file) as audio_track:
#         audio = rec.record(audio_track)
    
#     text = rec.recognize_google(audio,language="it-IT")
#     print(text)

def generate_soundwave_image(file):
    soundwave = wave.open(file,"r")
    # print(soundwave.getframerate())
    raw_audio = soundwave.readframes(-1)
    raw_audio = np.frombuffer(raw_audio,"int16")
    # print(raw_audio)
    # print(len(raw_audio))

    length = np.linspace(0,len(raw_audio) / soundwave.getframerate(), num=len(raw_audio))
    print(length)

    plt.figure(figsize=(20,5))
    # plt.title("Audio: {}".format(source)) #hide the title
    plt.plot(length,raw_audio)
    plt.axis('off') #hide axis

    filename = file.split('_')
    filename = filename[-1].split('.')[0]
    plt.savefig(f"../images/{filename}", transparent = True)






# convert_to_wav(source2)
generate_soundwave_image(source2)
