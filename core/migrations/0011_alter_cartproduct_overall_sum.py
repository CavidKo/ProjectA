# Generated by Django 4.2.5 on 2023-11-16 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_clothes_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='overall_sum',
            field=models.FloatField(null=True),
        ),
    ]
