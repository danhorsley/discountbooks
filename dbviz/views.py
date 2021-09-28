from django.shortcuts import render
from django.http import HttpResponse
from .plots import *


# Create your views here.

def home(request):
    html_plot1 = initial_plot()
    return render(request, 'home.html', {'html_plot1' : html_plot1})
