# from speech_recognition import Recognizer,AudioFile
import wave
import matplotlib.pyplot as plt
import numpy as np
import ffmpeg

source = "../audio/pronunciation_it_buongiorno.wav"
source2 = "../audio/imported/sound.wav"

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


def convert_to_wav_working_format(file):
    i = ffmpeg.input(file) #get input file path
    filename = file.split("/")[-1]
    filename = filename.split(".")[0]
    o = ffmpeg.output(i,f"../audio/{filename}.wav") #get output file path
    ffmpeg.run(o) #run the command
    print("successful")



convert_to_wav_working_format(source2)
# generate_soundwave_image(source2)
