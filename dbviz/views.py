from django.shortcuts import render
from django.http import HttpResponse
from .plots import *
from .pop import *


# Create your views here.

def home(request):
    html_plot1 = initial_plot()
    html_plot2 = first_order()
    html_plot3 = pvi()
    return render(request, 'home.html', {'html_plot1' : html_plot1,
                                        'html_plot2' : html_plot2,
                                          'html_plot3' : html_plot3})

def populate(request):
    pop_static(reset = False)
    pop_invoice(reset = False)
    pop_analysis(reset = False)
    pop_skumap(reset = False)
    pop_sales(reset = False)
    return render(request, 'populate.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def dataquery(request):
    return render(request, 'dataquery.html')

def viz(request):
    return render(request, 'viz.html')