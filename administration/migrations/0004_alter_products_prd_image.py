# Generated by Django 4.0 on 2021-12-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='prd_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
