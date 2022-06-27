# Generated by Django 3.2.13 on 2022-06-26 05:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_quote_quote_text_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='quote_opencv_file',
            field=models.ImageField(blank=True, null=True, upload_to='opencv', validators=[django.core.validators.validate_image_file_extension, django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])], verbose_name='Changed photo'),
        ),
    ]