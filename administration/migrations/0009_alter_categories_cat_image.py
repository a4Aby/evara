# Generated by Django 4.0.1 on 2022-01-12 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0008_categories_cat_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='cat_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
