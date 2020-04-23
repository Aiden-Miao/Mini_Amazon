# Generated by Django 3.0.2 on 2020-04-23 01:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AmazonWeb', '0004_auto_20200422_0108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='inventory',
        ),
        migrations.AddField(
            model_name='order',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AmazonWeb.Warehouse'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='truck',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AmazonWeb.Warehouse'),
        ),
        migrations.AlterField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AmazonWeb.Product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.TextField(default='in progress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='x_location',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='y_location',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='WhInventory',
        ),
    ]
