from django.urls import path
from .views import convert_file_to_jpg, convert_file_to_png, convert_file_to_gif, success_view, error_view, download_file, convert_mov_to_mp4

app_name = 'extension'

urlpatterns = [
    path('convert_mov_to_mp4/', convert_mov_to_mp4, name='convert_mov_to_mp4'),
    path('convertjpg/', convert_file_to_jpg, name='convert_file_to_jpg'),
    path('convertpng/', convert_file_to_png, name='convert_file_to_png'),
    path('convertgif/', convert_file_to_gif, name='convert_file_to_gif'),
    path('download/<path:file_path>/', download_file, name='download'),
    path('success/<path:file_path>/', success_view, name='success'),
    path('error/', error_view, name='error'),
]