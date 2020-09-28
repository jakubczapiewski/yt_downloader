from yt_downloader import views
from django.urls import path

urlpatterns = [
    path('create_request/', views.create_request, name='create-request'),
    path('download_progress/<uuid:pk>/', views.download_progress, name='download-progress'),
    path('download/<uuid:pk>/', views.download_file, name='download'),
]
