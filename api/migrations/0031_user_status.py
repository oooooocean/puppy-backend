# Generated by Django 4.0.4 on 2022-06-10 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_user_fans_alter_complain_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(choices=[(0, 'UserStatus.NORMAL'), (1, 'UserStatus.BLOCKING')], default=0, verbose_name='状态'),
        ),
    ]
