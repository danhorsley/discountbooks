# Generated by Django 3.2.7 on 2021-09-23 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbviz', '0002_analysisdata_idmap_inovicedata_salesdata'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InoviceData',
            new_name='InvoiceData',
        ),
    ]