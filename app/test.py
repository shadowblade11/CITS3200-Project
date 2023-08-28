import subprocess
import ffmpeg
from pydub import AudioSegment
src = "../audio/sound.mp3"
dst = "../audio/test.wav"
i = ffmpeg.input(src) #get input file path
o = ffmpeg.output(i,dst) #get output file path

ffmpeg.run(o) #run the command