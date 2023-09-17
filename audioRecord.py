### RECORDING AUDIO ####
import sounddevice as sd
from scipy.io.wavfile import write
import os

#sampling frequency
freq = 44100

#recording duration
duration = 5

#start recorder
print("\nRecording audio now.... .... ....\n")
recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

#recording....
sd.wait()
print("\nRecording Completed!\n")

#convert to audio for saving
title = "sample.wav"
write(title, freq, recording)
os.system("ffmpeg -i %s recording.wav" % title + "> /dev/null 2>&1")
os.system("rm sample.wav")

