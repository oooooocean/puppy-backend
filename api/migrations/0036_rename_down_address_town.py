# Generated by Django 4.0.4 on 2022-06-24 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='down',
            new_name='town',
        ),
    ]
