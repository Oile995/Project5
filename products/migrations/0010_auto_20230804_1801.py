# Generated by Django 3.2.20 on 2023-08-04 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20230803_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification',
            field=models.CharField(max_length=1000),
        ),
    ]
