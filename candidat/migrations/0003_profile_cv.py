# Generated by Django 5.0 on 2023-12-21 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidat', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cv',
            field=models.FileField(null=True, upload_to='cv/'),
        ),
    ]
