# Generated by Django 4.2.7 on 2023-12-11 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_tags_tag_az_tags_tag_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategories',
            name='category_az',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='blogcategories',
            name='category_en',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
