from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.student_login, name='login'),
    path('test/', views.mcq_test, name='mcq_test'),
    path('review/', views.review, name='review'),   # new route
]
