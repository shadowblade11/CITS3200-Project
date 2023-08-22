import subprocess

def getPhone(audioFile):
    phones = subprocess.check_output("python -m allosaurus.run -i %s" % audioFile, shell=True, encoding="utf-8")
    print(phones)

if __name__ == '__main__':
    source = "recording.wav"
    submittedAudio = "recording1.wav"

    getPhone(source)
    getPhone(submittedAudio)