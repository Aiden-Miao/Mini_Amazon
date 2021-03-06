# Generated by Django 3.0.2 on 2020-04-23 22:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name', max_length=200)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_location', models.IntegerField()),
                ('y_location', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truck_num', models.IntegerField()),
                ('warehouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='amazonweb.Warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myaddress_x', models.IntegerField(default=0, null=True)),
                ('myaddress_y', models.IntegerField(default=0, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
                ('dst_x', models.IntegerField()),
                ('dst_y', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('is_processed', models.BooleanField(default=False)),
                ('status', models.TextField(default='in progress')),
                ('truck_id', models.IntegerField(null=True)),
                ('products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='amazonweb.Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='amazonweb.Warehouse')),
            ],
        ),
    ]
