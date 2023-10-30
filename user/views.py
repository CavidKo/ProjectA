from django.shortcuts import render, redirect
from user.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def register(request):
    context = {
        'form': RegisterForm(),
    }
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if password != form.cleaned_data.get('password2'):
                context['error'] = 'Parollar eyni deyil!'
                return render(request, 'register.html', context)
            else:
                user = form.save()
                user.set_password(password)
                form.save()
                # context['form'] = RegisterForm()
                return redirect('home')
        else:
            context['error'] = form.errors
            print(form.errors)
    return render(request, 'register.html', context)


def user_login(request):
    form = LoginForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('home')
            else:
                context['error'] = 'Username or password is incorrect'
                return render(request, 'login.html', context)
        else:
            context['error'] = form.errors
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')