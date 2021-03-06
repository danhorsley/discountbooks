from .models import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
from matplotlib.patches import Rectangle, Patch
from datetime import datetime, timezone, timedelta, date
import time
import calendar
import numpy as np
import csv
import mpld3
from django.db.models import F, Count, Sum, Max, Min, FloatField
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth, ExtractWeekDay

def dmy(eff):
    return f'{eff.year}-{eff.month:02d}-{eff.day:02d}'
def sqldate_to_datetime(my_date):
    return datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S+00:00').date() 

def sales_by_book():
    sales_agg = SalesData.objects.values('book_id').order_by('book_id')\
                                    .annotate(total_s=Sum('price'))\
                                    .annotate(total_pc=Sum('post_crd'))\
                                    .annotate(total_q=Sum('quantity'))\
                                    .annotate(total_f=Sum('salesfees'))\
                                    .annotate(total_post=Sum('postage'))

    invoice_agg = InvoiceData.objects.values('book_id').order_by('book_id')\
                .annotate(total_inv_cost=Sum(F('cost')*F('quantity')))\
                .annotate(total_inv_qty=Sum(F('quantity')))\
                .annotate(wavg_cost = (F('total_inv_cost')/F('total_inv_qty')))

    invoice_dict = {y['book_id']:[y['total_inv_cost'], y['total_inv_qty'], 
                                y['wavg_cost']] for y in invoice_agg}

    static_dict = {x[0]: [x[2], x[1], x[4], x[5]] for x in StaticData.objects.values_list()}
    ana_dict = {y[1]: [y[6], y[3], y[4], y[5]] for y in AnalysisData.objects.values_list()}
    
    all_info = [[z['book_id'], 
                static_dict[z['book_id']][0], static_dict[z['book_id']][1], 
                static_dict[z['book_id']][2], static_dict[z['book_id']][3], 
                z['total_s'], z['total_pc'], z['total_q'], z['total_f'], z['total_post'],
                invoice_dict[z['book_id']][0], invoice_dict[z['book_id']][1],
                invoice_dict[z['book_id']][2], 
                z['total_s'] + z['total_pc'] + z['total_f'] + z['total_post'] - (invoice_dict[z['book_id']][2]*z['total_q']),
                (z['total_s'] + z['total_pc']+ z['total_f'] + z['total_post'] - (invoice_dict[z['book_id']][2]*z['total_q']))/z['total_q'],
                (z['total_s'] + z['total_pc']+ z['total_f'] + z['total_post'] - (invoice_dict[z['book_id']][2]*z['total_q']))/(z['total_q']*invoice_dict[z['book_id']][2]),
                ana_dict[z['book_id']][0], ana_dict[z['book_id']][1],
                ana_dict[z['book_id']][2], ana_dict[z['book_id']][3]]\
                for z in sales_agg]
        
    return np.core.records.fromrecords(all_info, 
                                     names=['isbn13', 'Title', 'Cover', 'PubDate',
                                             'Genre', 'Sales', 'Quantity', 'Fees', 'Postage',
                                             'tic', 'tiq', 'wavgc', 'Profit',
                                             'Profit_per_item', 'Margin',
                                             'ASR', 'Offers', '90d', 'Stock'])

def plot_format(my_plot):
    return my_plot.update_layout(autosize=False, width=800, height=493,
    legend_orientation="h", margin_t=25, margin_b=25, margin_r=25, margin_l=50,
    yaxis=go.layout.YAxis(titlefont=dict(size=15), tickformat='d'))


def initial_plot(my_html=True):
    my_asrs = []
    my_offers = []
    plt.switch_backend('Agg')
    with open("dbviz/analysis.csv", "r", encoding="ISO-8859-1") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                my_asrs.append(min(2.5,float(row[6])/1000000))
                my_offers.append(int(row[3]))
    fig, ax = plt.subplots(figsize=(4, 3.5))
    ax.scatter(my_asrs, my_offers, alpha=0.5)
    ax.set_xlabel('Sales rank in million (maxed at 2.5 million)', fontsize=12)
    ax.set_ylabel('Competing Offers', fontsize=12)
    ax.set_title(f'Scatter Plot of Sales rank vs Competing Offers')
    ax.add_patch(Rectangle((0, 0), 0.75, 7, facecolor="red"))
    red_patch = Patch(color='red', label='Target Zone')
    plt.legend(handles=[red_patch])
    if my_html: return mpld3.fig_to_html(fig)
    else: return plt.show()

def first_order(my_html=True):
    #this is for the second plot which contains four subplots
    fi = InvoiceData.objects.filter(date='2020-11-11').values_list()
    isbn_list = [x[1] for x in fi]
    ana_dict = {y[1]:[y[6], y[3]] for y in AnalysisData.objects.filter(book_id__in=isbn_list).values_list()}
    stat_dict = {z[0]:[z[2], z[5]] for z in StaticData.objects.filter(isbn13__in=isbn_list).values_list()}
    mq = SalesData.objects.filter(book_id__in=isbn_list)\
                                .annotate(my_profit = F('price') + F('post_crd') -0.4 \
                                + F('postage') + F('salesfees'))\
                                .values_list()
    order_qty = {y[1]:y[2] for y in fi}
    #create array of only relevant sales
    final_arr = np.empty((0,11))
    arr = np.array(mq).copy()
    for item in isbn_list:
        final_arr = np.append(final_arr, arr[arr[:,1]==item][:order_qty[item]], axis=0)
    final_arr = final_arr[final_arr[:, 2].argsort()]

    #data for first chart
    cumulative_profit = -232.75 + np.cumsum([x[10] for x in final_arr]) 
    dates = mdates.date2num([y[2] for y in final_arr])
    #data for second chart - profit by book
    totals_by_book = []
    for item in isbn_list:
        filt = final_arr[final_arr[:,1]==item].copy()
        totals_by_book.append([stat_dict[item], order_qty[item], np.sum(filt[:, 3]), 
                                np.sum(filt[:,10])-((order_qty[item]-np.sum(filt[:, 3]))*0.25), 
                                ana_dict[item]])
    #grid template for plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)  
   # ax1.xaxis_date()
    #first chart - cumulative profit over time with only buys and sales from first order 
    
    cmap = plt.get_cmap('RdBu')
    ax1.plot(dates, cumulative_profit)
    ax1.fill_between(dates, 0, cumulative_profit, where=cumulative_profit>0, facecolor='#5DADE2', interpolate=True)
    ax1.fill_between(dates, 0, cumulative_profit, where=cumulative_profit<=0, facecolor='#EC7063', interpolate=True)
    ax1.set_ylabel('Profit in ??', fontsize=7)
    ax1.set_title(f'Cumulative profit Dec 20 to Aug 21', fontsize=9)
    ax1.xaxis_date()
    ax1.set_xticks([])
    
    #second chart - profit by book
    totals_by_book.sort(key=lambda x: x[3])
    x2 = [x[0][0] for x in totals_by_book]
    y2 = [y[3] for y in totals_by_book]
    my_c2 = [cmap(0.5+ z/30) for z in y2]
    ax2.bar(x2, y2, color=my_c2)
    ax2.xaxis.set_visible(False)
    ax2.set_ylabel('Profit in ??', fontsize=7)
    ax2.set_title(f'Profit by name', fontsize=9)
    ax2.set_xticks([])
    #3rd chart profitability vs asr scatter
    x3 = [min(1,x[4][0]/1000000) for x in totals_by_book]
    y3 = [y[3] for y in totals_by_book]
    colours3 = np.where(np.array(y3)<=0,'r','b')
    my_c3 = [cmap(0.5+z/30) for z in y2]
    ax3.scatter(x3,y3,c=my_c2)
    ax3.set_xlabel('Sales rank in millions', fontsize=7)
    ax3.set_ylabel('Profit in ??', fontsize=7)
    ax3.set_title(f'Profit vs Sales rank', fontsize=9)
    #4th chart profitability vs asr scatter
    x4 = [x[4][1] for x in totals_by_book]
    y4 = [y[3] for y in totals_by_book]
    ax4.scatter(x4,y4, c=my_c2)
    ax4.set_xlabel('Number of competing offers', fontsize=7)
    ax4.set_ylabel('Profit in ??', fontsize=7)
    ax4.set_title(f'Offers vs Sales rank', fontsize=9)
    
    fig.tight_layout()
   
    
    if my_html: return mpld3.fig_to_html(fig)
    else: return plt.show()

def pvi(my_html=True):
    plt.switch_backend('Agg')
    group_inv = InvoiceData.objects.values('date').order_by('date')\
                                    .annotate(spend = -Sum('totalprice'))
    sales_ts = SalesData.objects.values('date').order_by('date')\
                .annotate(income = Sum(F('price') + F('post_crd') + F('salesfees') + F('postage')))

    ts = [[x['date'], x['income']]for x in sales_ts]
    ts += [[datetime(x['date'].year, x['date'].month, x['date'].day, tzinfo=timezone.utc), x['spend']]for x in group_inv]
    ts.sort(key=lambda x: x[0])
    ts_dates = [x[0] for x in ts]
    ts_cashflow = np.cumsum([x[1] for x in ts])
    
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ts_dates, ts_cashflow, alpha=0.5)
    myFmt = mdates.DateFormatter('%b')
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_ylabel('Profit in ??', fontsize=7)
    ax.set_title(f'Cashflow over time', fontsize=9)
    if my_html: return mpld3.fig_to_html(fig)
    else: return plt.show()


def ndq(my_title='', timeperiod='all_time', measure='profit',
                        my_ts = 'daily', cumulative = 'cumulative', my_html=True):
    #this is for the diy dataquery page - using numpy where possible to speed things up
    if my_title=='all titles': my_title =''                    
    time_max = date(2021, 8, 28)
    time_min = date(2020, 11, 12)
    time_dict = {'all_time' : time_max-time_min, 'all time' : time_max-time_min, 
                '7d' : timedelta(days = 7), '30d' : timedelta(days = 30),
                '90d': timedelta(days = 90), '180d': timedelta(days = 180)}
    ts_dict =  {'daily' : 0, 'by weekday': 1, 'by month' : 2, 'by year' : 3}
    arr = np.array(SalesData.objects.filter(book_id__title__contains=my_title,
            date__range=[dmy(time_max-time_dict[timeperiod]), dmy(time_max)])\
            .values_list())
    arr = np.c_[arr, [(x.date()-time_min).days for x in arr[:,2]],
                        [x.weekday() for x in arr[:,2]], 
                        [f'{x.month}-{x.year % 2000}' for x in arr[:,2]], 
                        [x.year for x in arr[:,2]]]
    n = 10+ ts_dict[my_ts]
    if measure=='profit': m = 9
    else: m = 3
    col_min = np.min(arr[:,n])
    my_measure = np.array(arr[:,m].copy(), dtype = 'float')
    
    if my_ts=='by month': 
        my_grouping = np.array(arr[:,n].copy())
        mg_unique=[]
        for mg in my_grouping:
            if mg not in mg_unique:
                mg_unique.append(mg)
        month_nums = {x[0]:x[1] for x in enumerate(mg_unique)}
        num_months = {x[1]:x[0] for x in enumerate(mg_unique)}
        my_grouping = np.array([num_months[x] for x in my_grouping],dtype = 'int64')
    else: my_grouping = np.array(arr[:,n].copy()- col_min, dtype = 'int64')
    my_agg = np.bincount(my_grouping, weights=my_measure)
    
    if my_ts == 'daily': my_x = [time_min + timedelta(int(x)+col_min) for x in range(len(my_agg))]
    elif my_ts=='by weekday' : my_x = [calendar.day_name[x+col_min] for x in range(len(my_agg))]
    elif my_ts=='by month' : my_x = [month_nums[x] for x in range(len(my_agg))]
    else: my_x = [x+col_min for x in range(len(my_agg))]
    if my_ts in ['by weekday', 'by year']: cumulative = 'distinct'
    #print(len(my_agg), len(my_x), print(my_x))
    if cumulative == 'distinct':
        my_plot = go.Figure(data=[go.Bar(x=my_x, y=list(my_agg))])
    else:
        my_choice = my_agg.cumsum()
        my_plot = go.Figure(data=[go.Scatter(x=my_x,y=my_choice, fill='tonexty')])
    my_plot.update_layout(autosize=False, width=800, height=493,
    legend_orientation="h",margin_t=25,margin_b=25,margin_r=25,margin_l=50,
    yaxis=go.layout.YAxis(titlefont=dict(size=15),tickformat="d"))
    if my_html : return my_plot.to_html()
    else: return my_plot.show()

    def mon_format(my_delta,my_start):
        new_date = my_start + timedelta(days=my_delta)
        return f'{new_date.month}-{new_date.year}'
