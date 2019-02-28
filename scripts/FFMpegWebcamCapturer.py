import ffmpeg
import numpy as np
from fire import Fire

class FFMpegWebcamCapturer:

    def __init__(self):
        return

    def facetime(self):
        (
            ffmpeg
            .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30, s='1280x720')
            .output('out.mp4', pix_fmt='yuv420p')
            .overwrite_output()
            .run()
        )

    def captureWebCam(self, out_filename: str, width, height):
        process1 = (
            ffmpeg
            .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30)
            .output('pipe:', format='rawvideo', pix_fmt='uyvy422')
            .run_async(pipe_stdout=True)
            )


        process2 = (
            ffmpeg
#            .input('pipe:', format='rawvideo', pix_fmt='uyvy422', s='{}x{}'.format(width, height))
            .input('pipe:', format='rawvideo', pix_fmt='uyvy422', s='1280x720')
            .output(out_filename, format='mp4', pix_fmt='yuv420p')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        while True:
            in_bytes = process1.stdout.read(width * height)
            if not in_bytes:
                break
            in_frame = (
                np
                .frombuffer(in_bytes, np.uint8)
                .reshape([height, width])
            )
            out_frame = in_frame
            process2.stdin.write(
                out_frame
                .astype(np.uint8)
                .tobytes()
            )
        process2.stdin.close()
        process1.wait()
        process2.wait()


if __name__ == "__main__":
    Fire(FFMpegWebcamCapturer)
