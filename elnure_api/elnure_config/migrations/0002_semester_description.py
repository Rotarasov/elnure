# Generated by Django 4.0.5 on 2022-06-16 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elnure_config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
