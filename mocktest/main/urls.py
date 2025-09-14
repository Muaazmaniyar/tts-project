from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('start_test/', views.start_test, name='start_test'),
    path("test/", views.mcq_test, name="mcq_test"),
    path("result/", views.result, name="result"),
    path('review/', views.review, name='review'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('test_history/', views.test_history, name='test_history'),
    path('progress/', views.student_progress, name='student_progress'),

       # new route
]
