from django.urls import path, include

urlpatterns = [
    path('', include('yt_downloader.urls')),
]
