from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('welcome/', views.dashboard_welcome, name='dashboard_welcome'),
    path('user/', views.dashboard_user, name='dashboard_user'),
    path('admin/', views.dashboard_admin, name='dashboard_admin'),
    path('logout/', views.logout_view, name='logout'),
]
