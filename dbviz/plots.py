from .models import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle, Patch
import numpy as np
import csv
import mpld3
from django.db.models import F, Count, Sum, Max, Min, FloatField

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

def sales_chart(how = 'best', many = 15, measure = 'profit'):
    m_dict = {'profit' : 12, 'quantity' : 6}
    sbb = sales_by_book()
    ordered_sales = [[x[1][:22], x[m_dict[measure]]] for x in sbb]
    ordered_sales.sort(key=lambda x: x[1])
    if how == 'best': myf = ordered_sales[-many:]
    else: myf = ordered_sales[:many]
    my_plot = go.Figure(data=[go.Bar(x=[x[0] for x in myf], 
                        y=[x[1] for x in myf])])
    plot_format(my_plot)
    return my_plot.show() 
 
def genre_chart():
    sbb = sales_by_book()



def plot_gen(my_x='ASR', my_y='Quantity', my_z = 'Profit', 
                my_hue = 'Genre', hover = 'Title',sbb=''):
    #generic plot
    
    def minner(my_list): return [min(x, 1000000) for x in my_list]
    if sbb=='': sbb = sales_by_book()
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(set(sbb[my_hue]))))
    coldict = {list(set(sbb[my_hue]))[i]:colors[i] for i in range(len(list(set(sbb[my_hue]))))}
    colplot = [coldict[x] for x in sbb[my_hue]]
    fig, ax = plt.subplots()
    ax.scatter(minner(sbb[my_x]), sbb[my_y], c=colplot, alpha=0.5)
    ax.set_xlabel(my_x, fontsize=15)
    ax.set_ylabel(my_y, fontsize=15)
    ax.set_title(f'{my_x} vs {my_y}')

    return plt.show()

def class_bar_plot(sbb, my_class='Genre', my_calc= 'Profit'):
    my_plot = go.Figure(data=[go.Bar(x=sbb[my_class], y=sbb[my_calc])])
    return my_plot.show()

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
    ax.set_xlabel('ASR in million (maxed at 2.5 million)', fontsize=12)
    ax.set_ylabel('Competing Offers', fontsize=12)
    ax.set_title(f'Scatter Plot of ASRs vs Competing Offers')
    ax.add_patch(Rectangle((0, 0), 0.75, 7, facecolor="red"))
    red_patch = Patch(color='red', label='Target Zone')
    plt.legend(handles=[red_patch])
    if my_html: return mpld3.fig_to_html(fig)
    else: return plt.show()

def first_order():
    fi = InvoiceData.objects.filter(date='2020-11-11').values_list()
    isbn_list = [x[1] for x in fi]
    mq = SalesData.objects.filter(book_id__in=isbn_list)\
                                .annotate(profit = F('price') + F('post_crd') -0.4 \
                                + F('postage') + F('salesfees'))\
                                .values_list()
    order_qty = {y[1]:y[2] for y in fi}
    final_arr = np.empty((0,9))
    arr = np.array(mq).copy()
    for item in isbn_list:
        final_arr = np.append(final_arr, arr[arr[:,1]==item][:order_qty[item]], axis=0)
    final_arr = final_arr[final_arr[:, 2].argsort()]
        
    cumulative_profit = -232.75 + np.cumsum([x[8] for x in final_arr]) 
    dates = mdates.date2num([y[2] for y in final_arr])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.plot(dates, cumulative_profit)
    plt.gcf().autofmt_xdate()
    return plt.show()