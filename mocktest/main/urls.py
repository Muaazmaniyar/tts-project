from django.urls import path
from . import views

urlpatterns = [
   # path('login/', views.login_page, name='login'),
   # path('adminpanel/', views.adminpanel, name='adminpanel'),
     path("review/", views.review, name="review"),
    path('', views.student_login, name="student_login"),
    path('dashboard/', views.student_dashboard, name="student_dashboard"),
    path('logout/', views.student_logout, name="student_logout"),
]
