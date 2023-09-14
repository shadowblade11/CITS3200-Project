import wave
import matplotlib.pyplot as plt
import numpy as np
import ffmpeg
import librosa
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

import os

def convert_to_wav_working_format(input_file,output_file):
    try:
        print(input_file)
        print(output_file)
        threshold = "-50dB" #need to mess around with threshold
        flag = f"areverse,atrim=start=0,silenceremove=start_periods=1:start_silence=0.1:start_threshold={threshold}"
        i = ffmpeg.input(input_file) #get input file path
        o = ffmpeg.output(i,output_file,af=f"{flag},{flag}") #get output file path, also removes the silent noise
        ffmpeg.run(o, overwrite_output=True, quiet=True) #run the command
        return 0
    except ffmpeg._run.Error as e:
        print(e)
        return -1



def compare(audio1, audio2):
    reference_audio, _ = librosa.load(audio1, sr=None)
    user_audio, _ = librosa.load(audio2, sr=None)
    # print(reference_audio,user_audio)

    mfcc_reference = librosa.feature.mfcc(y=reference_audio)
    mfcc_user = librosa.feature.mfcc(y=user_audio)

    distance, _ = fastdtw(mfcc_reference.T,mfcc_user.T, dist = euclidean)
    max_length = max(mfcc_reference.shape[1], mfcc_user.shape[1])
    similarity_score = 1 - (distance / max_length)

    print(similarity_score)

    distance = np.linalg.norm(np.mean(mfcc_reference, axis=1) - np.mean(mfcc_user, axis=1))
    max_distance = 1000  # Adjust this value based on your data and desired scoring range
    similarity_score = 10 - (10 * distance / max_distance)
    
    print(similarity_score)




def get_global_normalisation_param(audio_list):
    amplitudes_list = []
    for audio_file in audio_list:
        path = f"../audio/{audio_file}"
        audio, _ = librosa.load(path, sr=None)
        max_amplitude = np.max(np.abs(audio))
        amplitudes_list.append(max_amplitude)
    print(amplitudes_list)
    return max(amplitudes_list)


# def normalise_audio(audio_list, value):
#     for audio_file in audio_list:
#         path = f"../audio/{audio_file}"
#         audio, sr = librosa.load(path, sr=None)
#         normalized_audio = audio/value
#         normalized_audio_file = f"../audio/normalised/{audio_file}"
        

#this would be encapulated into a function once it is linked to the html page
list_of_audio = ["1 come ti chiami.m4a","2 come stai.m4a","3 questo e Matteo.m4a", "sound.wav"]
filename=list_of_audio[0]
filename,suffix = filename.split(".")

if suffix != "wav":
    path = "../audio/"
    src = path+f"/imported/{filename}.{suffix}"
    dst = path+f"{filename}.wav"
else:
    path = "../audio/"
    src = path+f"/imported/{filename}.wav"
    dst = path+f"{filename}.wav"


list_of_audio_2 = ["1 come ti chiami.wav","2 come stai.wav","3 questo e Matteo.wav", "sound.wav"]

# v = get_global_normalisation_param(list_of_audio_2)
# normalise_audio(list_of_audio_2,v)



# compare("../audio/1 come ti chiami.wav","../audio/1 come ti chiami.wav")


#actual functions to run
# convert_to_wav_working_format(src,filename)
# generate_soundwave_image(dst,filename)
