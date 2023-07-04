from django.urls import path
from .views.admin_views import shelf_views, db_test, admin_views, stock_views, sales_views
from .views.user_views import main_views, start_views

app_name = 'BLC'

urlpatterns = [
    path('', main_views.show_main_page, name='main'),
    path('start', start_views.show_start_page, name='start'),
    path('video_start/', start_views.video_start, name='video_start'),
    path('get_amount/', start_views.get_amount, name='get_amount'),
    path('process_payment/', start_views.process_payment, name='process_payment'),
    
    path('admin/', admin_views.show_main_page, name='admin_main'),
    path('admin/stock/', stock_views.show_stock_page, name='stock'),
    path('admin/shelf/', shelf_views.show_shelf_page, name='shelf'),
    path('admin/shelf/grid_video_start/', shelf_views.grid_video_start, name='grid_video_start'),
    path('admin/shelf/init_shelf_no', shelf_views.init_shelf_no, name='init_shelf_no'),
    path('admin/sales/', sales_views.show_sales_page, name='sales'),
    
]
