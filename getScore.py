from audioToText import convertAudio
from VowelsAndConsonants import getCandV

if __name__ == "__main__":
    sourceFile = 'audiofiles_wav/Come_Ti_Chiami.wav'
    submittedFile = 'recording.wav'

    print("\nAssessing now.... Please wait...\n")
    score1 = convertAudio(sourceFile, submittedFile)
    score2 = getCandV(sourceFile, submittedFile)

    OverallScore = round((score1 * 0.5) + (score2 * 0.5))
    print("Your score is:", OverallScore, "\n")
