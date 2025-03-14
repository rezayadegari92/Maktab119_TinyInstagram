import email
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def register_page(request):
    return render(request, 'register.html')

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('posts')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                # Validate next_page
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect('posts')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')




def profilesview(request):
    return render(request, 'profiles.html')