import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from yt_downloader.views import create_request, download_progress, download_file


class TestDownloadRequest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.create_view = create_request
        self.download_progress_view = download_progress
        self.create_url = r'./create_request/'
        self.progress_url = r'./create_request/'

    def test_get(self):
        data = json.dumps({'url': 'https://youtu.be/iSutodqCZ74'})
        request = self.factory.post(self.create_url, data=data, content_type="application/json")
        response = self.create_view(request)
        assert response.status_code == status.HTTP_200_OK
        request = self.factory.post(self.progress_url, content_type="application/json")
        response = self.download_progress_view(request, str(response.data))
        assert response.status_code == status.HTTP_200_OK
