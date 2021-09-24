from django.db import models

# Create your models here.
class StaticData(models.Model):
    isbn13 = models.CharField(max_length=15, primary_key=True)
    cover = models.CharField(max_length=13)
    title = models.CharField(max_length=200)
    isbn10 = models.CharField(max_length=13)
    pubdate = models.DateField()
    genre1 = models.CharField(max_length=30)
    genre2 = models.CharField(max_length=30)
    length = models.FloatField(default=200)
    width = models.FloatField(default=160)
    thick = models.FloatField(default=22)
    weight = models.FloatField(default=360)

class InvoiceData(models.Model):
    book = models.ForeignKey(StaticData, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    cost = models.FloatField(default=1)
    totalprice = models.FloatField(default=1)
    date = models.DateField()
    wholesaler = models.CharField(max_length=1)

class SkuMap(models.Model):
    book = models.ForeignKey(StaticData, on_delete=models.CASCADE, default=0)
    sku = models.CharField(max_length=13)


class SalesData(models.Model):
    sku = models.ForeignKey(SkuMap, on_delete=models.CASCADE, default=0)
    date = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=1)
    salesfees = models.FloatField(default=0)
    postage = models.FloatField(default=0)

class AnalysisData(models.Model):
    book = models.ForeignKey(StaticData, on_delete=models.CASCADE, default=0)
    sellpx = models.FloatField(default=1)
    offers = models.IntegerField(default=1)
    ninetyd = models.IntegerField(default=1)
    stock = models.IntegerField(default=1)
    asr = models.IntegerField(default=2000000)
    