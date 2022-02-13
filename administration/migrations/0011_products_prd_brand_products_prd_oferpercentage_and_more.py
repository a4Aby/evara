# Generated by Django 4.0.1 on 2022-01-19 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0010_productimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='prd_brand',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='products',
            name='prd_oferPercentage',
            field=models.FloatField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='products',
            name='prd_reviewsCount',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='products',
            name='proParent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='administration.products'),
        ),
    ]