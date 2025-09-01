from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('start_test/', views.start_test, name='start_test'),
    path('test/', views.mcq_test, name='mcq_test'),
    path('review/', views.review, name='review'),
    path('dashboard/', views.student_dashboard, name='dashboard'),   # new route
]
