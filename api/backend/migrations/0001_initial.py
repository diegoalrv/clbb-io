# Generated by Django 4.1 on 2023-12-11 22:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('aruco_id', models.PositiveIntegerField(default=0)),
                ('aruco_marker', models.ImageField(blank=True, null=True, upload_to='aruco_markers/')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('aruco_id', models.PositiveIntegerField(default=0)),
                ('aruco_marker', models.ImageField(blank=True, null=True, upload_to='aruco_markers/')),
                ('position_on_map', models.PositiveIntegerField(default=0)),
                ('lego_image', models.ImageField(blank=True, null=True, upload_to='lego/')),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('slider', models.PositiveIntegerField()),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('image', models.ImageField(upload_to='maps/')),
                ('coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.coin')),
                ('slot1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot1', to='backend.slot')),
                ('slot2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot2', to='backend.slot')),
                ('slot3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot3', to='backend.slot')),
                ('slot4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot4', to='backend.slot')),
                ('slot5', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot5', to='backend.slot')),
                ('slot6', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot6', to='backend.slot')),
                ('slot7', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot7', to='backend.slot')),
            ],
        ),
    ]