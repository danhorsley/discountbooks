from .models import *
from .utils import *
import os
import csv
import pytz
from datetime import datetime
from django.db.models import F, Count, Sum

def dateconverter(my_date, type = 'inv'):
        if type == 'inv':
            return datetime.strptime(my_date, '%d/%m/%Y')
        elif type == 'sales':
            return datetime.strptime(my_date, '%d-%m-%Y %H:%M:%S UTC')
        else:
            return datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S+00:00')

def pop_static(reset = True):
    if reset:
        StaticData.objects.all().delete()  
    with open("dbviz/static.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                #print(row[2])
                sd = StaticData(
                        isbn13 = str(row[0]), cover = row[1],
                        title = row[2][:200], isbn10 = toISBN10(row[0]),
                        pubdate = dateconverter(row[4]), genre1 = row[5],
                        genre2 = row[6], length = row[7],
                        width = row[8],thick = row[9], weight = row[10])
                sd.save()

def wac_dict(my_how = 'isbn'):
    if my_how == 'title': my_how = 'book_id__title'
    if my_how == 'isbn': my_how = 'book_id'
    invoice_agg = InvoiceData.objects.values(my_how).order_by(my_how)\
                .annotate(total_inv_cost=Sum(F('cost')*F('quantity')))\
                .annotate(total_inv_qty=Sum(F('quantity')))\
                .annotate(wavg_cost = (F('total_inv_cost')/F('total_inv_qty')))
    invoice_dict = {y[my_how][:21]:[y['total_inv_cost'], y['total_inv_qty'], 
                                y['wavg_cost']] for y in invoice_agg}
    return invoice_dict

def pop_sales(reset = True):
    sku_dict = {i[2] : i[1] for i in SkuMap.objects.all().values_list()}
    cost_dict = wac_dict()
    if reset:
        SalesData.objects.all().delete()
    with open("dbviz/sales.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if float(row[9]) == 0 : 
                    my_postage = -2.8
                else : 
                    my_postage = row[9]
                sd = SalesData(book = StaticData.objects.filter(isbn13=sku_dict[row[2]])[0],
                                date = datetime.strptime(row[0], '%d %b %Y %H:%M:%S %Z').replace(tzinfo=pytz.UTC), 
                                quantity = row[4], price = row[6], post_crd = row[7],
                                salesfees = row[8], postage = my_postage, 
                                wac = -cost_dict[sku_dict[row[2]]][2], 
                profit = float(row[6])+float(row[7])+float(row[8])+float(my_postage)-cost_dict[sku_dict[row[2]]][2])
                sd.save()

def pop_skumap(reset = True):
    if reset:
        SkuMap.objects.all().delete() 
    with open("dbviz/skumap.csv", "r") as f:
        reader = csv.reader(f)
        counter = -1
        for row in reader:
            counter += 1
            if counter ==0: pass
            else:
                my_isbn10 = '0'*(10-len(row[1])) + str(row[1])
                print(my_isbn10)
                sm = SkuMap(book = StaticData.objects.filter(isbn10=my_isbn10)[0],
                            sku = row[0], status = row[4])
                sm.save()

def pop_analysis(reset = True):
    if reset:
        AnalysisData.objects.all().delete()  
    counter = -1
    with open("dbviz/analysis.csv", "r", encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        for row in reader:
                counter +=1
                if counter ==0:
                    pass
                else:
                    print(row[0])
                    #print(not StaticData.objects.filter(isbn13=row[0]))
                    if not StaticData.objects.filter(isbn13=row[0]):
                        pass
                    else:
                        ad = AnalysisData(book = StaticData.objects.filter(isbn13=row[0])[0], 
                            sellpx = row[2], offers = row[3], ninetyd = row[4],
                            stock = row[5], asr = row[6])
                        ad.save()

def pop_invoice(reset = True):
    if reset:
        InvoiceData.objects.all().delete()  
    with open("dbviz/invoicedata.csv", "r") as f:
            reader = csv.reader(f)
            counter = -1
            for row in reader:
                counter += 1
                if counter == 0:
                    pass
                else:
                    #print(row[0])
                    invd = InvoiceData(
                        book = StaticData.objects.filter(isbn13=row[0])[0], 
                        quantity = row[1],
                        title = row[2], cost = row[3],
                        totalprice = row[4], 
                        date = dateconverter(row[5]),
                        wholesaler = row[6])
                    invd.save()
