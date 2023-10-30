from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from core.forms import ContactForm



# Create your views here.
def login(request):
    return render(request, 'login.html') 


def index(request):
    product = Clothes.objects.all().filter(active=True)

    context = {
        'product': product
    }
    return render(request, 'index.html', context)

def contact(request):
    context = {
        'contact': ContactForm()
    }
    if request.method == 'POST':
        result = ContactForm(request.POST)
        if result.is_valid():
            result.save()
        else:
            print(result.errors)
    return render(request, 'contact.html', context)

def blog(request):
    return render(request, 'blog.html')

def product(request):
    return render(request, 'product.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'shoping-cart.html')
