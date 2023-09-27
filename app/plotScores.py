import wave
import matplotlib.pyplot as plt
import numpy as np

def generate_soundwave_image(file, output_path, filename):
    plt.switch_backend('Agg')
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
    
    plt.savefig(f"{output_path}/{filename}", transparent = True)
    plt.close()

    return 0
