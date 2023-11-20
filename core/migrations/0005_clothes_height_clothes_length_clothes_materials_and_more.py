# Generated by Django 4.2.5 on 2023-11-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_tags_clothes_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='height',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='clothes',
            name='length',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='clothes',
            name='materials',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='clothes',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='clothes',
            name='width',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
