# Generated by Django 3.0.8 on 2020-07-18 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20200718_2201'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='version',
            index=models.Index(fields=['published'], name='packages_ve_publish_09509d_idx'),
        ),
    ]
