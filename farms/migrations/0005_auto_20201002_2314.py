# Generated by Django 3.1.2 on 2020-10-02 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farms', '0004_auto_20201002_2301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datapoint',
            old_name='date_type',
            new_name='data_type',
        ),
    ]
