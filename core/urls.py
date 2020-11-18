from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.admin_login, name="admin_login"),
    path('logout', views.admin_logout, name="admin_logout"),
    path('getstats', views.get_stats, name="get_stats"),
]