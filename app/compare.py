import numpy as np
import librosa
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

import os

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