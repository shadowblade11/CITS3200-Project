import wave
import matplotlib.pyplot as plt
import numpy as np
import ffmpeg
import librosa
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

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
    # print(filename)
    plt.savefig(f"./static/images/{filename}", transparent = True)


def convert_to_wav_working_format(file,filename):
    i = ffmpeg.input(file) #get input file path
    # o = ffmpeg.output(i,f"../audio/{filename}.wav",af="silenceremove=1:0:-50dB") #get output file path, also removes the silent noise at the start
    o = ffmpeg.output(i,f"../audio/{filename}.wav") #no silent noise removed
    ffmpeg.run(o, overwrite_output=True, quiet=True) #run the command
    print("successful")


def compare(audio1, audio2):
    reference_audio, _ = librosa.load(audio1, sr=None)
    user_audio, _ = librosa.load(audio2, sr=True)
    # print(reference_audio,user_audio)

    mfcc_reference = librosa.feature.mfcc(y=reference_audio)
    mfcc_user = librosa.feature.mfcc(y=user_audio)

    distance, _ = fastdtw(mfcc_reference.T,mfcc_user.T, dist = euclidean)
    max_length = max(mfcc_reference.shape[1], mfcc_user.shape[1])
    similarity_score = 1 - (distance / max_length)

    print(similarity_score)



#this would be encapulated into a function once it is linked to the html page
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

compare("../audio/1 come ti chiami.wav","../audio/1 come ti chiami.wav")


#actual functions to run
# convert_to_wav_working_format(src,filename)
# generate_soundwave_image(dst,filename)
