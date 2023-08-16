import subprocess
import numpy

#seconds to sample audio for
sampleTime = 5

#number of points to scan cross correlation over
span = 150

#step size in points for cross correlation
step = 1

#minimum number of point that must overlap
minOverlap = 20

#report match when cross correlation has a preak excceding threshold
threshold = 0.5

#calculating fingerprint
def calculateFingerprint(filename):
    fpcalc = subprocess.check_outputc('fpcalc -raw -length %i %s' % (sampleTime, filename))
    fingerprintIndex = fpcalc.find('FINGERPRINT=') + 12
    fingerprints = map(int, fpcalc[fingerprintIndex].split(','))

    return fingerprints

#returning correlation between lists
def correlation(x, y):
    if len(x) == 0 or len(y) == 0:
        raise Exception('Empty lists cannot be correlated.')
    if len(x) > len(y) :
        x = x[:len(y)]
    elif len(x) < len(y):
        y = y[:len(x)]

    covariance = 0

    for i in range(len(x)):
        covariance += 32 - bin(x[i] ^ y[i]).count("1")
    covariance = covariance / float(len(x))

    return covariance/32

#return cross correlation, with y offset from x
def crossCorrelation(x,y,offset):
    if offset > 0:
        x = x[offset:]
        y = y[:len(x)]
    
    elif offset < 0:
        offset = -offset 
        y = y[offset:]
        x = x[:len(y)]
    if min(len(x), len(y)) < minOverlap:
        #should not reach here
        return
    
    return correlation(x,y)

def compare(x,y,span,step):
    if span > min(len(x), len(y)):

        raise Exception('span >= sample size: %i >= %i\n'
                        % (span, min(len(x), len(y)))
                        + 'Reduce span, reduce crop or increase sample_time.')

    corrXY = []

    for offset in numpy.arrange(-span, span + 1, step):
        corrXY.append(crossCorrelation(x,y,offset))
    return corrXY

#return index of max value in list
def maxIndex(x):
    maxIndex = 0
    maxValue = x[0]
    for i, value in enumerate(x):
        if value > maxValue:
            maxValue = value
            maxIndex = i 
    return maxIndex

def getMaxCorr(corr, source, target):
    maxCorrIndex = maxIndex(corr)
    maxCorrOffset = -span + maxCorrIndex * step
    print("max corr index = ", maxCorrIndex, "max corr offset = ", maxCorrOffset)

    if corr[maxCorrIndex] > threshold:
        print('%s and %s match with correlation of %.4f at offset %i' % (source, target, corr[maxCorrIndex], maxCorrOffset))

def correlate(source, target):
    fingerprintSource = calculateFingerprint(source)
    fingerprtinTarget = calculateFingerprint(target)

    corr = compare(fingerprintSource, fingerprtinTarget, span, step)
    maxCorrOffset = getMaxCorr(corr,source,target)


