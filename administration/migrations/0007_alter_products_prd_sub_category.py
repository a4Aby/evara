# Generated by Django 3.2.6 on 2022-01-08 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0006_products_prd_is_featured_products_prd_is_popular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='prd_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.categories'),
        ),
    ]