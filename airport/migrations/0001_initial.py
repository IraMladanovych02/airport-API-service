# Generated by Django 4.0.4 on 2024-09-23 06:50

import airport.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'facilities',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=255, null=True)),
                ('num_seats', models.IntegerField()),
                ('image', models.ImageField(null=True, upload_to=airport.models.image_path)),
                ('facilities', models.ManyToManyField(related_name='plays', to='airport.facility')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('departure', models.DateTimeField()),
                ('plane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport.plane')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport.order')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport.trip')),
            ],
            options={
                'ordering': ('seat',),
            },
        ),
    ]
