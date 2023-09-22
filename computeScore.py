from audioToText import convertAudio
from analyseDF import getScores


if __name__ == "__main__":
    sourceFile = 'audiofiles_wav/Come_Ti_Chiami.wav'
    submittedFile = 'audiofiles_wav/molto_bene_grazie.wav'

    print("\nAssessing now.... Please wait...\n")
    audio_to_text_score = convertAudio(sourceFile, submittedFile)
    ratio_score, duration_score = getScores(sourceFile, submittedFile)

    OverallScore = round((audio_to_text_score * 0.45) + (ratio_score * 0.25) + (duration_score * 0.30))
    print("Your score is:", OverallScore, "\n")
