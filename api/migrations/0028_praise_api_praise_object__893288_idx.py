# Generated by Django 4.0.4 on 2022-06-09 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_alter_praise_options_praise_one_praise_one_target'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='praise',
            index=models.Index(fields=['object_id', 'content_type'], name='api_praise_object__893288_idx'),
        ),
    ]