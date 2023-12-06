# Generated by Django 4.2.5 on 2023-11-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_clothes_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='category_az',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='category_en',
        ),
        migrations.RemoveField(
            model_name='colors',
            name='color_az',
        ),
        migrations.RemoveField(
            model_name='colors',
            name='color_en',
        ),
        migrations.RemoveField(
            model_name='sizes',
            name='size_az',
        ),
        migrations.RemoveField(
            model_name='sizes',
            name='size_en',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='tag_az',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='tag_en',
        ),
        migrations.AlterField(
            model_name='clothes',
            name='size',
            field=models.ManyToManyField(to='core.sizes'),
        ),
    ]