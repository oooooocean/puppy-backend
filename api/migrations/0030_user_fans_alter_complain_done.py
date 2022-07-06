# Generated by Django 4.0.4 on 2022-06-10 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_complain_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fans',
            field=models.ManyToManyField(related_name='idols', to='api.user'),
        ),
        migrations.AlterField(
            model_name='complain',
            name='done',
            field=models.BooleanField(default=False, verbose_name='是否已处理'),
        ),
    ]
