from yt_downloader.models import VideoRequest
from rest_framework import serializers


class VideoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRequest
        fields = '__all__'
