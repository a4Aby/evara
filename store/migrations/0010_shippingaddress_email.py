# Generated by Django 4.0.1 on 2022-02-05 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_shippingaddress_address2_shippingaddress_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
