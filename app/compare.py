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
    # o = ffmpeg.output(i,f"../audio/{filename}",af="silenceremove=1:0:-50dB") #get output file path, also removes the silent noise at the start
    o = ffmpeg.output(i,f"../audio/{filename}") #no silent noise removed
    ffmpeg.run(o, overwrite_output=True, quiet=True) #run the command
    print("successful")


list_of_audio = ["sound.wav","buon_pomeriggio.wav","buongiorno.wav"]
filename=list_of_audio[1]
path = "../audio/"
src = path+f"/imported/{filename}"
dst = path+f"{filename}"

convert_to_wav_working_format(src,filename)
generate_soundwave_image(dst,filename)
