# Generated by Django 4.0.4 on 2022-05-28 10:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elnure_core', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='elective_groups',
        ),
        migrations.AddField(
            model_name='block',
            name='capacity',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.CreateModel(
            name='ElectiveGroupStudentAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('choice', models.ForeignKey(help_text='Student choice which this asssociation is created for', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='final_distributions', to='elnure_core.choice')),
                ('elective_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_associations', to='elnure_core.electivegroup')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elective_group_associations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'elective_group_student_associations',
            },
        ),
    ]