from audioToText import convertAudio
from analyseDF import getScores


if __name__ == "__main__":
    sourceFile = 'audio/1_come_ti_chiami.wav'
    submittedFile = 'audio/1_come_ti_chiami.wav'

    print("\nAssessing now.... Please wait...\n")
    audio_to_text_score = convertAudio(sourceFile, submittedFile)
    ratio_score, duration_score, phone_score = getScores(sourceFile, submittedFile)
    #just to see the individual scores returned
    print(audio_to_text_score,ratio_score, duration_score, phone_score)

    OverallScore = round((audio_to_text_score * 0.45) + (ratio_score * 0.18) + (duration_score * 0.18) + (phone_score * 0.19))
    print("Your score is:", OverallScore, "\n")
