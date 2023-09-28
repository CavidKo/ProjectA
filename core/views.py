from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
        'title': 'Home',
        'heading': 'Welcome to home page'
    }
    return render(request, 'index.html', context)
