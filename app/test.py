import subprocess
import ffmpeg
from pydub import AudioSegment
src = "../audio/sound.mp3"
dst = "../audio/test.wav"
i = ffmpeg.input(src)
o = ffmpeg.output(i,dst)
# print(o)
ffmpeg.run(o)
# convert wav to mp3                                                            
# sound = AudioSegment.from_mp3(src)
# sound.export(dst, format="wav")
# input_file = ffmpeg.input("../audio/sound.mp3")
# subprocess.run(f".\ffmpeg.exe -version")