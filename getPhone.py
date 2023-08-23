import subprocess

def checkPronounciation(sourcePhone, submittedPhone):
    matchedPhone = 0
    print(len(sourcePhone))
    print(len(submittedPhone))
    if len(sourcePhone) >= len(submittedPhone):
        longString = sourcePhone
        shortString = submittedPhone
    else:
        longString = submittedPhone
        shortString = sourcePhone
    
    for i in range(len(longString)):
        if (i < len(shortString)):
            if (sourcePhone[i] == submittedPhone[i]):
                matchedPhone += 1
    
    score = matchedPhone / len(longString)    
    print(score)

def getPhone(audioFile):
    phones = subprocess.check_output("python -m allosaurus.run -i %s" % audioFile, shell=True, encoding="utf-8")
    print(phones)
    return phones

if __name__ == '__main__':
    source = "recording.wav"
    submittedAudio = "recording1.wav"
    sourcePhone = getPhone(source)
    submittedPhone = getPhone(submittedAudio)

    checkPronounciation(sourcePhone, submittedPhone)