#USAGE: python compare.py -i SOURCEFILE -o TARGETFILE

import argparse
from correlation import correlate

def initialise():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--source-file", help="source file")
    parser.add_argument("-o", "--target-file", help="target file")
    args = parser.parse_args()

    SOURCEFILE = args.source_file if args.source_file else None
    TARGETFILE = args.target_file if args.target_file else None

    if not SOURCEFILE or not TARGETFILE:
        raise Exception("Source or Target files not specified")
    
    return SOURCEFILE, TARGETFILE

if __name__ == "__main__" :
    SOURCEFILE, TARGETFILE = initialise()
    correlate(SOURCEFILE, TARGETFILE)

    

