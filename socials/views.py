from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def posts(request):
    return render(request, "posts1.html")