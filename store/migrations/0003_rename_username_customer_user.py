# Generated by Django 4.0 on 2021-12-29 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_user_customer_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='username',
            new_name='user',
        ),
    ]
