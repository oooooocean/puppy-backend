# Generated by Django 4.0.4 on 2022-06-09 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_praise_api_praise_object__893288_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.user'),
            preserve_default=False,
        ),
    ]
