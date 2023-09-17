import ffmpeg




def convert_to_wav_working_format(input_file, output_file):
    try:
        threshold = "-50dB"  # need to mess around with threshold
        flag = f"areverse,atrim=start=0,silenceremove=start_periods=1:start_silence=0.1:start_threshold={threshold}"
        i = ffmpeg.input(input_file)  # get input file path
        o = ffmpeg.output(i, output_file, af=f"{flag},{flag}")  # get output file path, also removes the silent noise
        ffmpeg.run(o, overwrite_output=True)  # run the command TODO remember to add quiet=True
        return 0
    except ffmpeg._run.Error as e:
        print(e)
        return -1