# Generated by Django 3.2.7 on 2021-09-28 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbviz', '0009_analysisdata_wholesaler'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysisdata',
            name='wholesaler',
        ),
    ]
