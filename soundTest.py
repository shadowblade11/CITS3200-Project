### RECORDING AUDIO ####
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

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
title = "recording.wav"
write(title, freq, recording)

### PLAYING AUDIO ### 
#need to download ffmpeg to work
from pydub import AudioSegment
from pydub.playback import play

#playing mp3 audio
if ".wav" in title:
    audio = AudioSegment.from_wav("recording.wav")
else:
    audio = AudioSegment.from_mp3("recording.wav")
print("Playing audio now.... .... ....\n")
play(audio)
