# Generated by Django 4.2.5 on 2023-11-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_clothes_color_clothes_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='info',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
