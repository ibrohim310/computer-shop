# Generated by Django 5.0.6 on 2024-05-18 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_qr_code_image_product_qr_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]