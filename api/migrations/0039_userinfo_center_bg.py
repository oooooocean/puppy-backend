# Generated by Django 4.0.4 on 2022-06-28 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_rename_postnotices_user_post_notices'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='center_bg',
            field=models.CharField(blank=True, max_length=500, verbose_name='个人中心背景'),
        ),
    ]