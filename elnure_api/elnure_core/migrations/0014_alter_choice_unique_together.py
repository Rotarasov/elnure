# Generated by Django 4.0.5 on 2022-06-16 16:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elnure_config', '0002_semester_description'),
        ('elnure_core', '0013_remove_block_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('student', 'application_window', 'semester')},
        ),
    ]
