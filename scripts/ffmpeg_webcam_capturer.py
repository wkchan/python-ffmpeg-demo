""" A Module for evaluating ffmpeg-python """

import ffmpeg
import numpy as np
from fire import Fire


class FFMpegWebcamCapturer:
    """ A class for utilising python-ffmpeg """

    def __init__(self):
        pass
    @staticmethod
    def facetime():
        """ facetime function is designed for capturing video from facetime
        camera and store it into a video
        """
        (
            ffmpeg
            .input('FaceTime', format='avfoundation', pix_fmt='yuv420p', framerate=30, s='1280x720')
            .output('out.mp4', pix_fmt='yuv420p', video_bitrate='1024000', preset='veryfast')
            .overwrite_output()
            .run()
        )

    @staticmethod
    def capture_web_cam(out_filename: str, width: int = 1280, height: int = 720):
        """ capture_web_cam function is design for capturing the video from facetime camera
        and process it with a numpy function.
        After processing it, the video will be saved in a file
        """

        process1 = ffmpeg \
            .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30) \
            .output('pipe:', format='rawvideo', pix_fmt='uyvy422') \
            .run_async(pipe_stdout=True)

        process2 = ffmpeg \
            .input('pipe:', format='rawvideo', pix_fmt='uyvy422', s='{}x{}'.format(width, height)) \
            .output(out_filename, format='mp4', pix_fmt='yuv420p') \
            .overwrite_output() \
            .run_async(pipe_stdin=True)

        in_bytes = process1.stdout.read(width * height)
        while in_bytes:
            in_frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width])
            process2.stdin.write(in_frame.astype(np.uint8).tobytes())
            in_bytes = process1.stdout.read(width * height)
        process2.stdin.close()
        process1.wait()
        process2.wait()


if __name__ == "__main__":
    Fire(FFMpegWebcamCapturer)
