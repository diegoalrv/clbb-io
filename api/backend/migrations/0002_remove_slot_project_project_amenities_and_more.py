# Generated by Django 4.1 on 2023-12-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='amenities',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='aruco_marker',
            field=models.ImageField(blank=True, null=True, upload_to='aruco_markers/'),
        ),
        migrations.AddField(
            model_name='slot',
            name='lego_image',
            field=models.ImageField(blank=True, null=True, upload_to='lego/'),
        ),
    ]
