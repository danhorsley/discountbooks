from .models import *
import os
import csv
from datetime import datetime

def dateconverter(my_date, type = 'inv'):
        if type == 'inv':
            return datetime.strptime(my_date, '%d/%m/%Y')
        else:
            return datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S+00:00')

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
                    bd = InvoiceData(
                        isbn13 = row[0], quantity = row[1],
                        title = row[2], cost = row[3],
                        totalprice = row[4], date = dateconverter(row[5]),
                        wholesaler = row[6])
                    bd.save()
