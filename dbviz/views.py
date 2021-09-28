from django.shortcuts import render
from django.http import HttpResponse
from .plots import *
from .pop import *


# Create your views here.

def home(request):
    html_plot1 = initial_plot()
    return render(request, 'home.html', {'html_plot1' : html_plot1})

def populate(request):
    pop_static()
    pop_invoice()
    pop_analysis()
    pop_skumap()
    pop_sales()
    return render(request, 'populate.html')