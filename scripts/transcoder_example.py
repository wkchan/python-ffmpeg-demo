""" A Module for evaluating ffmpeg-python """
# import boto3
import ffmpeg
import os
from fire import Fire
from managers.aws_manager import AWSManager


class TranscoderExample:
    """ A class for utilising python-ffmpeg """

    def __init__(self):
        pass

    def transcode_to_CMAF2(input_path: str, output_dir: str, width: int = 1280, height: int = 720):
        """transcode a video to CMAF for HLS and MPEGDASH

        Arguments:
            input_path {str} -- source file path
            out_filename {str} -- output file path

        Keyword Arguments:
            width {int} -- video width resolution (default: {1280})
            height {int} -- video height resolution (default: {720})
        """

        output_dir = os.path.abspath(output_dir)
        output_mpd = os.path.join(output_dir, 'output.mpd')
        size = '{}x{}'.format(width, height)

        print(output_mpd)
        (
            ffmpeg
            .input(input_path)
            .output(
                output_mpd, pix_fmt="yuv420p", video_bitrate='1024000', f='dash',
                vcodec="libx264", preset="fast", s="1280x720", acodec="aac", audio_bitrate="128000", hls_playlist="1")
            .overwrite_output()
            .run()
        )
#        for file in os.listdir(output_dir):
#            print(file)
#            AWSManager.upload_file_to_s3(file, 'kiwi-pycon-x-origin')

    @staticmethod
    def transcode_to_CMAF(input_path: str, output_dir: str, s3_bucket_name: str = 'kiwi-pycon-x-origin', width: int = 1280, height: int = 720):
        """transcode a video to CMAF for HLS and MPEGDASH

        Arguments:
            input_path {str} -- source file path
            out_filename {str} -- output file path

        Keyword Arguments:
            width {int} -- video width resolution (default: {1280})
            height {int} -- video height resolution (default: {720})
        """

        if (not os.path.isdir):
            os.mkdir(output_dir)

        buckets = AWSManager.list_s3_buckets()
        if not (s3_bucket_name in buckets):
            AWSManager.create_s3_bucket(s3_bucket_name)

        out_filename = os.path.join(output_dir, 'output.mpd')
        (
            ffmpeg
            .input(input_path)
            .output(
                out_filename, pix_fmt='yuv420p', video_bitrate='1024000', f='dash',
                vcodec='libx264', preset='fast', acodec="aac", audio_bitrate="128000", hls_playlist="1")
            .overwrite_output()
            .run()
        )
        for file in os.listdir(output_dir):
            print(file)
            AWSManager.upload_file_to_s3(os.path.join(output_dir, file), s3_bucket_name, file)


if __name__ == "__main__":
    Fire(TranscoderExample)
