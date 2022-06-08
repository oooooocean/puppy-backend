# Generated by Django 4.0.4 on 2022-06-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_posttopic_audit_status_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttopic',
            name='audit_description',
            field=models.CharField(max_length=200, null=True, verbose_name='审核意见'),
        ),
        migrations.AlterField(
            model_name='posttopic',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='topics', to='api.post'),
        ),
        migrations.DeleteModel(
            name='TopicAuditRecord',
        ),
    ]