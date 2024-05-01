# main/urls.py
from django.urls import path
from .views import base_view, profile_view, drive_view, another_page_view, logout_view, delete_file , view_file , home , login , register
# welcome_view
# login_signup_view
urlpatterns = [
    path('', home, name='index'),
    # path('welcome_view/', welcome_view, name='welcome'),
    path('base/', base_view, name='base'),
    # path('login/', login_signup_view, name='login_signup'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', profile_view, name='profile'),
    path('drive/', drive_view, name='drive'),
    path('another_page/', another_page_view, name='another_page'),
    path('logout/', logout_view, name='logout'),
    path('delete_file/<int:file_id>/', delete_file, name='delete_file'),  # Add this line
    path('view/<int:fid>/', view_file, name='view_file'),
    
    # Add more paths as needed
]
