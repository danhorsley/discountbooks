from .models import *
import plotly.graph_objects as go
from django.db.models import F, Count, Sum, Max, Min, FloatField

def dmy(eff):
    return f'{eff.year}-{eff.month:02d}-{eff.day:02d}'
def sqldate_to_datetime(my_date):
    return datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S+00:00').date() 

def sales_by_book():
    sales_agg = SalesData.objects.values('book_id').order_by('book_id')\
                                    .annotate(total_s=Sum('price'))\
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
    
    all_info = [[z['book_id'], 
                static_dict[z['book_id']][0], static_dict[z['book_id']][1], 
                static_dict[z['book_id']][2], static_dict[z['book_id']][3], 
                z['total_s'], z['total_q'], z['total_f'], z['total_post'],
                invoice_dict[z['book_id']][0], invoice_dict[z['book_id']][1],
                invoice_dict[z['book_id']][2], 
                z['total_s'] + z['total_f'] + z['total_post'] - (invoice_dict[z['book_id']][2]*z['total_q'])]\
                for z in sales_agg]
        
    return all_info

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

