# Generated by Django 3.1.2 on 2020-10-24 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201024_2308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='comment_content',
            new_name='content',
        ),
    ]
