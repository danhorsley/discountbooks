from .models import *
from .utils import *
import os
import csv
import pytz
from datetime import datetime

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

def pop_sales(reset = True):
    sku_dict = {i[2] : i[1] for i in SkuMap.objects.all().values_list()}
    if reset:
        SalesData.objects.all().delete()
    with open("dbviz/sales.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[9]==0 : my_postage = 2.8
                else : my_postage = row[9]
                sd = SalesData(book = StaticData.objects.filter(isbn13=sku_dict[row[2]])[0],
                                date = datetime.strptime(row[0], '%d %b %Y %H:%M:%S %Z').replace(tzinfo=pytz.UTC), 
                                quantity = row[4], price = row[6], 
                                salesfees = row[8], postage = my_postage)
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
                    print(row[0])
                    invd = InvoiceData(
                        book = StaticData.objects.filter(isbn13=row[0])[0], 
                        quantity = row[1],
                        title = row[2], cost = row[3],
                        totalprice = row[4], 
                        date = dateconverter(row[5]),
                        wholesaler = row[6])
                    invd.save()
