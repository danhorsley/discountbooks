# Generated by Django 3.2.7 on 2021-09-23 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbviz', '0003_rename_inovicedata_invoicedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicedata',
            name='date',
            field=models.DateField(),
        ),
    ]