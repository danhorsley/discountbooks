from .models import *
import plotly.graph_objects as go
from django.db.models import F, Count, Sum, Max, Min, FloatField

def dmy(eff):
    return f'{eff.year}-{eff.month:02d}-{eff.day:02d}'
def sqldate_to_datetime(my_date):
    return datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S+00:00').date() 

def sales_by_book():
    my_agg = StaticData.objects.values('title').order_by('title')\
                                    .annotate(total_s=Sum('salesdata__price'))\
                                    .annotate(total_q=Sum('salesdata__quantity'))\
                                    .annotate(total_f=Sum('salesdata__salesfees'))\
                                    .annotate(total_post=Sum('salesdata__postage'))\
                                    .annotate(total_inv_cost=Sum(F('invoicedata__cost')*F('invoicedata__quantity')))\
                                    .annotate(total_inv_qty=Sum(F('invoicedata__quantity')))\
                                    .annotate(wavg_cost = (F('total_inv_cost')/F('total_inv_qty')))\
        .annotate(total_p = (F('total_s') + F('total_f') + F('total_post') - (F('wavg_cost')*F('total_q'))))
    return my_agg

def plot_format(my_plot):
    return my_plot.update_layout(autosize=False, width=800, height=493,
    legend_orientation="h", margin_t=25, margin_b=25, margin_r=25, margin_l=50,
    yaxis=go.layout.YAxis(titlefont=dict(size=15), tickformat='d'))

def sales_chart(how = 'best', many = 15):
    sbb = sales_by_book()
    def no_none(s): return 0 if s is None else s
    ordered_sales = [[x['title'][:22], no_none(x['total_p'])] for x in sbb]
    ordered_sales.sort(key=lambda x: x[1])
    if how == 'best': myf = ordered_sales[-many:]
    else: myf = ordered_sales[:many]
    my_plot = go.Figure(data=[go.Bar(x=[x[0] for x in myf], 
                        y=[x[1] for x in myf])])
    plot_format(my_plot)
    return my_plot.show() 
 
