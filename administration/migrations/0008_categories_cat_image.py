# Generated by Django 4.0.1 on 2022-01-09 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_alter_products_prd_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='cat_image',
            field=models.CharField(default='', max_length=100),
        ),
    ]