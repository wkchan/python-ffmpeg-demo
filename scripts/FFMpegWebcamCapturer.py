import ffmpeg
import numpy as np
from fire import Fire


class FFMpegWebcamCapturer:

    def __init__(self):
        pass

    def facetime():
        ffmpeg \
            .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30, s='1280x720') \
            .output('out.mp4', pix_fmt='yuv420p') \
            .overwrite_output() \
            .run()

    def capture_web_cam(self, out_filename: str, width: int = 1280, height: int = 720):
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
