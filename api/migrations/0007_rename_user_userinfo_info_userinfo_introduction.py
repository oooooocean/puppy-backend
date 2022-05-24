# Generated by Django 4.0.4 on 2022-05-24 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_pet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='user',
            new_name='info',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='introduction',
            field=models.CharField(blank=True, max_length=200, verbose_name='宠物寄语'),
        ),
    ]
