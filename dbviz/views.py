from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
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
    pop_static()
    pop_invoice()
    pop_analysis()
    pop_skumap(r)
    pop_sales()
    return render(request, 'populate.html')

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'danielhorsley@me.com', ['danielhorsley@me.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("home")
      
	form = ContactForm()
	return render(request, "contact.html", {'form':form})

def about(request):
    return render(request, 'about.html')

def viz(request):
    return render(request, 'viz.html')

def dataquery(request):
    try:

        if request.POST['timeperiod'] == "all time":
            new_time_period = "all time"
        else:
            new_time_period = f"last {request.POST['timeperiod']}"
        html_plot = dq(my_title=request.POST['title'], timeperiod=request.POST['timeperiod'], 
                        measure=request.POST['measure'], my_ts = request.POST['timesplit'], 
                        cumulative =request.POST['cumulative'], my_html=True)
        default_sub = f"""{request.POST['timesplit'].capitalize()} {request.POST['measure']} of
                             {request.POST['title']} over {new_time_period} ({request.POST['cumulative']})"""
        default_menus = [request.POST['title'], request.POST['timesplit'],
                        request.POST['timeperiod'], request.POST['measure'],
                        request.POST['cumulative']]
    except:
        html_plot = dq()
        default_sub = "Make your own visualizations"
        default_menus = ['all titles', 'daily', 'all time', 'net profit', 'distinct']
    print(default_menus)
    title = list(set(StaticData.objects.values_list('title', flat=True))) #filter1 for title 
    title = list(set([x[:21] for x in title]))
    timesplit = ['daily', 'by weekday', 'by week', 'by month']
    time_period = ['all time', '7d', '30d', '90d', '180d'] #filter for time period
    measure = ['quantity', 'profit'] #quantity or net profit
    cumulative = ['distinct', 'cumulative']
    title.sort()
    title = ['all titles'] + title
    
    return render(request, 'dataquery.html', {'titles' : title , 'timesplit' : timesplit ,
                                                'time_period' : time_period,
                                                'measures' : measure,
                                                'cumulative' : cumulative,
                                                'html_plot' : html_plot,
                                                "default_sub" : default_sub,
                                                "default_menus" : default_menus
                                                })