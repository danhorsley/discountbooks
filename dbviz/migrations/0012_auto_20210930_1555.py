# Generated by Django 3.2.7 on 2021-09-30 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbviz', '0011_salesdata_post_crd'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdata',
            name='profit',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='salesdata',
            name='wac',
            field=models.FloatField(default=1),
        ),
    ]
