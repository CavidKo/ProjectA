# Generated by Django 4.2.5 on 2023-12-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_remove_blogcategories_category_az_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]