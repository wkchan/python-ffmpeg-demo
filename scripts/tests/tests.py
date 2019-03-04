import ffmpeg
import os

def test_ffprobe():
    """ This test is designed for testing the ffprobe availability
    """
    path = os.path.abspath('./scripts/tests/resources/BigBuckBunny_320x180.mp4')
    result = ffmpeg.probe(path)
    print(result)
    assert(type(result) is dict)

def test_ffmpeg():
    in_filepath = os.path.abspath('./tests/resources/BigBuckBunny_320x180.mp4')
    out_filepath = os.path.abspath('./tests/resources/BigBuckBunny_320x180_output.mp4')
    # ffmpeg.input(in_filepath).output(out_filepath, vcodec='copy', acodec='copy').overwrite_output().run()
    ffmpeg.input(in_filepath).output(out_filepath).overwrite_output().run()
    result = ffmpeg.probe(out_filepath)
    assert(type(result) is dict)
    os.remove(out_filepath)
