# Generated by Django 2.2.2 on 2019-07-24 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0005_shop_number_of_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='number_of_reviews',
        ),
    ]
