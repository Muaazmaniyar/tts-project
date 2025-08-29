from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('testpanel/', views.testpanel, name='testpanel'),
    path('adminpanel/', views.adminpanel, name='adminpanel'),
]
