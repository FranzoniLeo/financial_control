from django.shortcuts import render

def home(request):
    return render(request, 'landing/landing.html')

def about(request):
    return render(request, 'landing/about.html')
