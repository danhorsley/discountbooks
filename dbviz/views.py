from django.shortcuts import render
from django.http import HttpResponse
import markdown


# Create your views here.

def home(request):
    
    return render(request, 'home.html')
