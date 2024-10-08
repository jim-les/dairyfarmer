# urls.py in app

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vaccination/', views.vacination, name='vaccination'),
    path('milk/', views.vacination, name='milk'),
    path('settings/', views.vacination, name='settings'),
    path('add-vaccination/', views.add_vaccination, name='add_vaccination'),
    path('add_pending_task/', views.add_pending_task, name='add_pending_task'),
    path('milk-collection/', views.milk_collection, name='milk-collection'), 
    path('report', views.report, name='report'),
    path('logout/', views.logout_view, name='logout'),
]