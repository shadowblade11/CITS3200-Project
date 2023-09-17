from audioToText import convertAudio
from VowelsAndConsonants import getCandV

if __name__ == "__main__":
    sourceFile = 'audiofiles_wav/Come_stai.wav'
    submittedFile = 'audiofiles_wav/molto_bene_grazie.wav'

    score1 = convertAudio(sourceFile, submittedFile)
    score2 = getCandV(sourceFile, submittedFile)

    OverallScore = (score1 * 0.5) + (score2 * 0.5)
    print(OverallScore)
