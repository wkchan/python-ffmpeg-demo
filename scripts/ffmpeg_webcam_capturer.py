""" A Module for evaluating ffmpeg-python """

import ffmpeg
from fire import Fire


class FFMpegWebcamCapturer:
    """ A class for utilising python-ffmpeg """

    def __init__(self):
        pass

    @staticmethod
    def facetime_to_hls():
        """ facetime function is designed for capturing video from facetime
        camera and store it into a video
        """
        (
            ffmpeg
            .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30, s='1280x720')
            .output(
                '/Applications/MAMP/htdocs/hls/hlssample.m3u8', pix_fmt='yuv420p',
                video_bitrate='1024000', f='hls', vcodec='libx264', preset='fast',
                acodec="aac", audio_bitrate="128000", start_number=0, hls_time=10,
                hls_list_size=0)
            .overwrite_output()
            .run()
        )

    @staticmethod
    def screen_to_facebook(stream_key: str):
        """ Capture Screen in macOS and stream it to facebook
        """
        (
            ffmpeg
            .input('1:1', format='avfoundation', pix_fmt='uyvy422', framerate=30, s='1280x800')
            .output(
                'rtmps://live-api-s.facebook.com:443/rtmp/{}'.format(stream_key), s='640x400', pix_fmt='yuv420p', video_bitrate='500000', f='flv',
                vcodec='libx264', preset='fast', x264opts='keyint=15', g='30', acodec="aac", audio_bitrate="128000")
            .overwrite_output()
            .run()
        )

    @staticmethod
    def pip_to_facebook(stream_key: str):
        """ Capture Facetime camera in macOS and stream it to facebook
        """
        facetime_camera_input = (
            ffmpeg
            .input('FaceTime:1', format='avfoundation', pix_fmt='0rgb', framerate=30, s='320x240')
        )
        screen_input = (
            ffmpeg
            .input('1:1', format='avfoundation',
                   pix_fmt='0rgb', framerate=30, probesize='100M')
            .filter('scale', size='1280x800')
        )
        file_input = (
            ffmpeg
            .input('source.mp4')
        )
        (
            ffmpeg
            .input(thread_queue_size='512')
            .overlay(screen_input, facetime_camera_input, format='rgb', x=0, y=0)
            # facetime_camera_input.output(
            .output('rtmps://live-api-s.facebook.com:443/rtmp/{}'.format(stream_key), vsync='2', s='640x360', pix_fmt='yuv420p', video_bitrate='300000', f='flv',
                    # .output('output.mp4', vsync='2', s='640x360', pix_fmt='yuv420p', video_bitrate='500000', f='flv',
                    # vcodec='libx264', preset='superfast', x264opts='keyint=15', g='30', acodec="aac", audio_bitrate="128000")
                    vcodec='h264_videotoolbox', profile='baseline', level='1.3', g='30', acodec="aac", audio_bitrate="128000")
            # .output("output.mp4")
            .overwrite_output()
            .compile()
            # .run()
        )

    @staticmethod
    def facetime_to_facebook(stream_key: str):
        """ Capture Facetime camera in macOS and stream it to facebook
        """
        (
            ffmpeg
            .input('0:1', format='avfoundation', pix_fmt='uyvy422', framerate=30, s='1280x720')
            .output(
                'rtmps://live-api-s.facebook.com:443/rtmp/{}'.format(stream_key), s='640x360', pix_fmt='yuv420p', video_bitrate='500000', f='flv',
                vcodec='libx264', preset='fast', x264opts='keyint=15', g='30', acodec="aac", audio_bitrate="128000")
            .overwrite_output()
            .run()
        )

    @staticmethod
    def facetime_to_rtmp():
        """ facetime function is designed for capturing video from facetime
        camera and store it into a video
        """
        (
            ffmpeg
            .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30, s='1280x720')
            .output(
                'rtmp://127.0.0.1:1935/live', pix_fmt='yuv420p', video_bitrate='1024000', f='flv',
                vcodec='libx264', preset='fast', acodec="aac", audio_bitrate="128000")
            .overwrite_output()
            .run()
        )

    @staticmethod
    def facetime():
        """ facetime function is designed for capturing video from facetime
        camera and store it into a video
        """
        (
            ffmpeg
            .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30, s='1280x720')
            .output(
                'output.mp4', pix_fmt='yuv420p', video_bitrate='1024000', f='mp4',
                vcodec='libx264', preset='fast', acodec="aac", audio_bitrate="128000")
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

    @staticmethod
    def transcode_to_CMAF(input_path: str, out_filename: str, width: int = 1280, height: int = 720):
        """transcode a video to CMAF for HLS and MPEGDASH

        Arguments:
            input_path {str} -- source file path
            out_filename {str} -- output file path

        Keyword Arguments:
            width {int} -- video width resolution (default: {1280})
            height {int} -- video height resolution (default: {720})
        """

        (
            ffmpeg
            .input(input_path)
            .output(
                out_filename, pix_fmt='yuv420p', video_bitrate='1024000', f='dash',
                vcodec='libx264', preset='fast', acodec="aac", audio_bitrate="128000", hls_playlist="1")
            .overwrite_output()
            .run()
        )


if __name__ == "__main__":
    Fire(FFMpegWebcamCapturer)
