from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')

def adminpanel(request):
    return render(request, 'admin.html')
