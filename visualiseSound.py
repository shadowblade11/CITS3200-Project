import wave
import numpy as np
import matplotlib.pyplot as plt

def getGraph(audioFile):
    #read .wav file
    wavObject = wave.open(audioFile, "rb")

    sampleFreq = wavObject.getframerate() # sample rate
    nSamples = wavObject.getnframes() # individual sample rate
    tAudio = nSamples/sampleFreq # length of audio file
    
    nChannels = wavObject.getnchannels() # check number of audio channels
    signalWave = wavObject.readframes(nSamples) # value of signal wave (amplitude)

    #getting data from both channels and splitting it
    signalArr = np.frombuffer(signalWave,dtype=np.int16)
    lChannel = signalArr[0::2]
    rChannel = signalArr[1::2]

    times = np.linspace(0, nSamples/sampleFreq, num=nSamples) #time stamp for each signal

    # plotting signal for left channel
    plt.figure(figsize=(15,5)) 
    plt.plot(times, lChannel)
    plt.title("Left Channel")
    plt.ylabel("Signal Value")
    plt.xlabel("Time(s)")
    plt.xlim(0,tAudio)
    plt.show()


if __name__ == "__main__":
    getGraph("pronunciation_it_buon_pomeriggio.wav")
    getGraph("recording.wav")