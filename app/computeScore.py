from app.audioToText import convertAudio
from app.analyseDF import getScores

def compute_score(sourceFile, submittedFile):
    audio_to_text_score = convertAudio(sourceFile, submittedFile)
    ratio_score, duration_score, phone_score = getScores(sourceFile, submittedFile)

    OverallScore = round((audio_to_text_score * 0.45) + (ratio_score * 0.18) + (duration_score * 0.18) + (phone_score * 0.19))
    return OverallScore
