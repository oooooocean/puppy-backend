# Generated by Django 4.0.4 on 2022-06-27 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_user_postnotices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='postNotices',
            new_name='post_notices',
        ),
    ]