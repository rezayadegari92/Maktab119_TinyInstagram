from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def register_page(request):
    return render(request, 'register.html')

def home(request):
    return render(request, 'home.html')



def login(request):
    return render(request, 'login.html')
