# Generated by Django 4.0.4 on 2022-05-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userinfo_create_time_userinfo_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=1, max_length=11, verbose_name='手机号'),
            preserve_default=False,
        ),
    ]