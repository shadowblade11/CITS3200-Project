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
    filename = filename.split(".")[0]
    # print(filename)
    plt.savefig(f"../images/{filename}", transparent = True)


def convert_to_wav_working_format(file,filename):
    i = ffmpeg.input(file) #get input file path
    o = ffmpeg.output(i,f"../audio/{filename}") #get output file path
    ffmpeg.run(o,quiet=True, overwrite_output=True) #run the command
    print("successful")


filename="sound.wav"
path = "../audio/"
src = path+f"/imported/{filename}"
dst = path+f"{filename}"

convert_to_wav_working_format(src,filename)
generate_soundwave_image(dst,filename)
