from django.urls import path
from .views import main_views, start_views

app_name = 'BLC'

urlpatterns = [
    path('', main_views.show_main_page, name='main'),
    path('start', start_views.show_start_page, name='start'),
    path('video_start/', start_views.video_start, name='video_start'),

]   