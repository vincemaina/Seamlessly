def get_video_properties(file_path):

    import ffmpeg
    import sys

    try:
        probe = ffmpeg.probe(file_path)
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)

    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        print('No video stream found', file=sys.stderr)
        sys.exit(1)

    return video_stream
