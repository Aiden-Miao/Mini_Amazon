# Generated by Django 3.0.2 on 2020-04-22 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmazonWeb', '0003_auto_20200422_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='myaddress_x',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='myaddress_y',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='x_location',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='y_location',
            field=models.IntegerField(default=0),
        ),
    ]
