# Generated by Django 3.2.7 on 2021-09-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbviz', '0010_remove_analysisdata_wholesaler'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdata',
            name='post_crd',
            field=models.FloatField(default=0),
        ),
    ]
