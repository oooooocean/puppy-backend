# Generated by Django 4.0.4 on 2022-06-06 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_postcomplain'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomplain',
            options={'verbose_name': '帖子投诉'},
        ),
        migrations.AddField(
            model_name='postcomplain',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
