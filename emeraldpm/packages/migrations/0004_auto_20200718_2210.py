# Generated by Django 3.0.8 on 2020-07-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_auto_20200718_2209'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='downloadcount',
            index=models.Index(fields=['package'], name='packages_do_package_3aefc0_idx'),
        ),
    ]
