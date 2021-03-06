# Generated by Django 4.0 on 2021-12-14 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='Description',
            new_name='cat_description',
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='Name',
            new_name='cat_name',
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='Parent',
            new_name='cat_slug',
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='Slug',
            new_name='parent_category',
        ),
        migrations.AddField(
            model_name='categories',
            name='cat_order',
            field=models.CharField(default='1', max_length=10),
        ),
        migrations.AddField(
            model_name='categories',
            name='cat_status',
            field=models.CharField(default='1', max_length=10),
        ),
    ]
