# Generated by Django 3.2.7 on 2021-09-28 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbviz', '0008_auto_20210926_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisdata',
            name='wholesaler',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
