# Generated by Django 4.2.5 on 2023-11-15 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_clothes_height_clothes_length_clothes_materials_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='weight',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
