# Generated by Django 4.0 on 2021-12-15 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_rename_description_categories_cat_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prd_name', models.CharField(default='', max_length=255)),
                ('prd_description', models.TextField(default='')),
                ('prd_price', models.FloatField(default=0)),
                ('prd_strike_price', models.FloatField(default=0)),
                ('prd_currency', models.CharField(default='', max_length=100)),
                ('prd_gst', models.CharField(default='', max_length=100)),
                ('prd_cod_available', models.CharField(default='0', max_length=100)),
                ('prd_width', models.CharField(default='', max_length=100)),
                ('prd_height', models.CharField(default='', max_length=100)),
                ('prd_weight', models.CharField(default='', max_length=100)),
                ('prd_shipping_fee', models.CharField(default='', max_length=100)),
                ('prd_parent_category', models.CharField(default='', max_length=100)),
                ('prd_sub_category', models.CharField(default='', max_length=100)),
                ('prd_tags', models.CharField(default='', max_length=100)),
                ('prd_status', models.CharField(default='1', max_length=10)),
                ('prd_order', models.CharField(default='1', max_length=10)),
                ('prd_image', models.ImageField(blank=True, null=True, upload_to='assets/uploads/')),
                ('prd_created_on', models.DateField(auto_now_add=True)),
            ],
        ),
    ]