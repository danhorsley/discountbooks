# Generated by Django 3.2.7 on 2021-09-23 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticData',
            fields=[
                ('isbn13', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('cover', models.CharField(max_length=11)),
                ('title', models.CharField(max_length=200)),
                ('isbn10', models.CharField(max_length=13)),
                ('pubdate', models.DateTimeField()),
                ('cost', models.FloatField(default=1)),
                ('genre1', models.CharField(max_length=30)),
                ('genre2', models.CharField(max_length=30)),
                ('length', models.FloatField(default=200)),
                ('width', models.FloatField(default=160)),
                ('thick', models.FloatField(default=22)),
                ('weight', models.FloatField(default=360)),
            ],
        ),
    ]