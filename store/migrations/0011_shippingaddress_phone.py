# Generated by Django 4.0.1 on 2022-02-05 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_shippingaddress_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
