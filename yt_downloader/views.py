import os
import threading
import datetime

from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from yt_downloader.serializers import VideoRequestSerializer
from yt_downloader.models import VideoRequest
from yt_downloader.video_downloader import VideoDownloader
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@throttle_classes([AnonRateThrottle])
def create_request(request) -> Response:
    url = request.data.get('url', False)
    if not url:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    data = {'url': str(url), 'exist': True}
    serializer = VideoRequestSerializer(data=data)

    #  validation
    serializer.is_valid(raise_exception=True)
    serializer.save()
    try:
        stream = VideoDownloader.search_video(serializer.instance.url)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        if VideoDownloader.check_video_size(stream):
            t = threading.Thread(target=VideoDownloader.download_to_server, args=(stream, str(serializer.instance.id)))
            t.setName(str(serializer.instance.id))
            t.start()
        else:
            return Response('video_file_to_big', status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.instance.id)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@throttle_classes([AnonRateThrottle])
def download_progress(request, pk) -> Response:
    progress = get_object_or_404(VideoRequest, pk=pk).progress
    return Response(progress)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@throttle_classes([AnonRateThrottle])
def download_file(request, pk):
    file_path = os.path.dirname(os.path.realpath('download')) + '\\download\\files\\' + str(pk) + '.mp4'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
