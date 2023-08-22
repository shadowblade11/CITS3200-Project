import subprocess

def getPhone(audioFile):
    phone = subprocess.check_output("python -m allosaurus.run -i %s" % audioFile, shell=True)
    print(phone)

if __name__ == "__main__":
    source = "recording.wav"
    submittedAudio = "recording1.wav"

    getPhone(source)
    getPhone(submittedAudio)
