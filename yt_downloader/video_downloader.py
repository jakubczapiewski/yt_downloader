import datetime
import os
import threading

from yt_downloader.serializers import VideoRequestSerializer
from yt_downloader.models import VideoRequest
from pytube import YouTube


class VideoDownloader:
    Path = os.path.dirname(os.path.realpath('download')) + '\\download\\files\\'

    @staticmethod
    def progress_func(stream=None, chunk=None, bytes_remaining=None) -> None:
        try:
            pk = threading.current_thread().name
            size = stream.filesize
            progress = round((float(abs(bytes_remaining - size) / size)) * float(100))
            if progress != 100:
                request_video = VideoRequest.objects.get(pk=pk)
                serializer = VideoRequestSerializer(request_video, data={'progress': progress}, partial=True)
                if serializer.is_valid():
                    serializer.save()
        except:
            pass

    @staticmethod
    def complete_function(x, y) -> None:
        try:
            pk = threading.current_thread().name
            request_video = VideoRequest.objects.get(pk=pk)
            serializer = VideoRequestSerializer(request_video, data={'progress': 100}, partial=True)
            if serializer.is_valid():
                serializer.save()
            VideoDownloader.clean()
        except:
            pass

    # search video function
    @staticmethod
    def search_video(url: str) -> YouTube.streams:
        video_streams = YouTube(
            url,
            on_progress_callback=VideoDownloader.progress_func,
            on_complete_callback=VideoDownloader.complete_function
        )
        result = video_streams.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1]
        return result

    @staticmethod
    def check_video_size(video_stream: YouTube.streams) -> bool or str:
        if video_stream.filesize < 3000000000:
            return True
        else:
            return False

    # Download video to server
    @staticmethod
    def download_to_server(video_stream: YouTube.streams, file_name: str) -> bool:
        video_stream.download(filename=file_name, output_path=VideoDownloader.Path)
        return True

    @staticmethod
    def clean():
        video_list = list(
            VideoRequest.objects.filter(created__lt=datetime.datetime.now() - datetime.timedelta(days=1)).filter(
                file_exist=True))
        print(video_list)
        for video in video_list:
            pk = video.pk
            file_path = os.path.dirname(os.path.realpath('download')) + "\\download\\files\\" + str(pk) + '.mp4'
            if os.path.exists(file_path):
                os.remove(file_path)
                video.file_exist = False
                video.save()
            else:
                video.file_exist = False
                video.save()
