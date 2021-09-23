from django.db import models

# Create your models here.
class StaticData(models.Model):
    isbn13 = models.CharField(max_length=15, primary_key=True)
    cover = models.CharField(max_length=11)
    title = models.CharField(max_length=200)
    isbn10 = models.CharField(max_length=13)
    pubdate = models.DateTimeField()
    cost = models.FloatField(default=1)
    genre1 = models.CharField(max_length=30)
    genre2 = models.CharField(max_length=30)
    length = models.FloatField(default=200)
    width = models.FloatField(default=160)
    thick = models.FloatField(default=22)
    weight = models.FloatField(default=360)

class InvoiceData(models.Model):
    isbn13 = models.CharField(max_length=13)
    quantity = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    cost = models.FloatField(default=1)
    totalprice = models.FloatField(default=1)
    date = models.DateField()
    wholesaler = models.CharField(max_length=1)

class IdMap(models.Model):
    isbn10 = models.CharField(max_length=13)
    sku = models.CharField(max_length=13)


class SalesData(models.Model):
    sku = models.CharField(max_length=13) #will link to isbn10 later
    date = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=1)
    salesfees = models.FloatField(default=0)
    postage = models.FloatField(default=0)

class AnalysisData(models.Model):
    isbn13 = models.CharField(max_length=13)
    sellpx = models.FloatField(default=1)
    offers = models.IntegerField(default=1)
    ninetyd = models.IntegerField(default=1)
    stock = models.IntegerField(default=1)
    asr = models.IntegerField(default=2000000)
    