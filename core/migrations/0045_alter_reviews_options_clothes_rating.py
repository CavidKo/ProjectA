# Generated by Django 4.2.7 on 2023-12-11 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_reviews'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'verbose_name': 'Reviews', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AddField(
            model_name='clothes',
            name='rating',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
