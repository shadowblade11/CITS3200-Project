import wave
import matplotlib.pyplot as plt
import numpy as np
import ffmpeg

def generate_soundwave_image(file, filename):
    soundwave = wave.open(file,"r")
    # print(soundwave.getframerate())
    raw_audio = soundwave.readframes(-1)
    raw_audio = np.frombuffer(raw_audio,"int16")
    # print(raw_audio)
    # print(len(raw_audio))

    length = np.linspace(0,len(raw_audio) / soundwave.getframerate(), num=len(raw_audio))
    # print(length)

    plt.figure(figsize=(20,5))
    # plt.title("Audio: {}".format(source)) #hide the title
    plt.plot(length,raw_audio)
    plt.axis('off') #hide axis
    print(filename)
    plt.savefig(f"../images/{filename}", transparent = True)


def convert_to_wav_working_format(file,filename):
    i = ffmpeg.input(file) #get input file path
    # o = ffmpeg.output(i,f"../audio/{filename}.wav",af="silenceremove=1:0:-50dB") #get output file path, also removes the silent noise at the start
    o = ffmpeg.output(i,f"../audio/{filename}.wav") #no silent noise removed
    ffmpeg.run(o, overwrite_output=True, quiet=True) #run the command
    print("successful")


list_of_audio = ["1 come ti chiami.m4a","2 come stai.m4a","3 questo e Matteo.m4a"]
filename=list_of_audio[1]
filename,suffix = filename.split(".")

if suffix != "wav":
    path = "../audio/"
    src = path+f"/imported/{filename}.{suffix}"
    dst = path+f"{filename}.wav"
else:
    path = "../audio/"
    src = path+f"/imported/{filename}.wav"
    dst = path+f"{filename}.wav"

convert_to_wav_working_format(src,filename)
generate_soundwave_image(dst,filename)
