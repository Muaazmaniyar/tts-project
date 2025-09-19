from django.urls import path
from . import views
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from main.views import student_login, student_dashboard, change_password, student_logout,start_test,result,mcq_test,student_progress,review,test_history

urlpatterns = [
   path('', views.student_login, name='login'),
   path('change_password/', views.change_password, name='change_password'),
   path('logout/', views.student_logout, name='logout'),
   path("dashboard/", views.student_dashboard, name="dashboard"),
   path("change_password/", views.change_password, name="change_password"),
   path('start_test/', views.start_test, name='start_test'),
   path("test/", views.mcq_test, name="mcq_test"),
   path('progress/', views.student_progress, name='student_progress'),
   path("result/", views.result, name="result"),
   path('review/', views.review, name='review'),
   path('test_history/', views.test_history, name='test_history'),
]
