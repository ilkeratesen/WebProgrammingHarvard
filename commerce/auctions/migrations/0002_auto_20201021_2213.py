# Generated by Django 3.1.2 on 2020-10-21 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='image',
        ),
        migrations.AddField(
            model_name='listings',
            name='image1',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='listings',
            name='image2',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='listings',
            name='image3',
            field=models.URLField(blank=True),
        ),
    ]