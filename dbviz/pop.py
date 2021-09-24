from .models import *
from .utils import *
import os
import csv
from datetime import datetime

def dateconverter(my_date, type = 'inv'):
        if type == 'inv':
            return datetime.strptime(my_date, '%d/%m/%Y')
        else:
            return datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S+00:00')

def pop_static(reset = True):
    if reset:
        StaticData.objects.all().delete()  
    with open("dbviz/new_static.csv", "r") as f:
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
