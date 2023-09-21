from audioToText import convertAudio
from analyseDF import getScores


if __name__ == "__main__":
    sourceFile = 'audiofiles_wav/Come_Ti_Chiami.wav'
    submittedFile = 'audiofiles_wav/molto_bene_grazie.wav'

    print("\nAssessing now.... Please wait...\n")
    score1 = convertAudio(sourceFile, submittedFile)
    score2, score3 = getScores(sourceFile, submittedFile)

    OverallScore = round((score1 * 1/3) + (score2 * 1/3) + (score3 * 1/3))
    print("Your score is:", OverallScore, "\n")
