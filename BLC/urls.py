from django.urls import path
from .views import main_views, start_views, shelf_views

app_name = 'BLC'

urlpatterns = [
    path('', main_views.show_main_page, name='main'),
    path('start', start_views.show_start_page, name='start'),
    path('video_start/', start_views.video_start, name='video_start'),
    path('get_amount/', start_views.get_amount, name='get_amount'),
    path('shelf', shelf_views.show_shelf_page, name='shelf'),
    path('grid_video_start/', shelf_views.grid_video_start, name='grid_video_start'),
]
