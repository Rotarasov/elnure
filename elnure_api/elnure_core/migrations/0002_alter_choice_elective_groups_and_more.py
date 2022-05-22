# Generated by Django 4.0.4 on 2022-05-22 20:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elnure_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='elective_groups',
            field=models.ManyToManyField(help_text='Elective groups attached to students after groups formation', related_name='students_choices', to='elnure_core.electivegroup'),
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('student', 'application_window')},
        ),
    ]
