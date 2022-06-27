# Generated by Django 3.2.13 on 2022-06-27 10:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0010_quote_quote_opencv_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='book_category',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=2, message=None)], verbose_name='Category'),
        ),
    ]
