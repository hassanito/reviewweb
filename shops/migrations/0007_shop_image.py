# Generated by Django 2.2.2 on 2019-07-24 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0006_remove_shop_number_of_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
