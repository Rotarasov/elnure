# Generated by Django 4.0.4 on 2022-05-28 10:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import elnure_common.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elnure_config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('total_credits', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'db_table': 'blocks',
            },
        ),
        migrations.CreateModel(
            name='ElectiveCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('shortcut', models.CharField(max_length=10)),
                ('syllabus', models.CharField(max_length=300)),
                ('capacity', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('credits', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('performance_assessment', elnure_common.fields.ElnureEnumField(choices=[('SESSION_EXAMINATION', 'Session Examination'), ('GRADED_SEMESTER', 'Graded Semester')], default='GRADED_SEMESTER', max_length=19)),
                ('is_professional', models.BooleanField(default=True, help_text='Whether subject professional or humanitartian')),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='elnure_core.block')),
            ],
            options={
                'db_table': 'elective_courses',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'instructors',
            },
        ),
        migrations.CreateModel(
            name='StrategySnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semesters_snapshot', models.JSONField(help_text='Snapshot of semesters with blocks and elective courses for this strategy run')),
                ('strategy', elnure_common.fields.ElnureEnumField(choices=[('DEFAULT', 'Default'), ('OPTIMIZED', 'Optimized')], max_length=9)),
                ('result', models.JSONField(help_text='List of elective groups for elective subjects with students')),
                ('application_window_snapshot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strategy_run_results', to='elnure_config.applicationwindow')),
            ],
            options={
                'db_table': 'strategy_snapshots',
            },
        ),
        migrations.CreateModel(
            name='InstructorAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('position', elnure_common.fields.ElnureEnumField(choices=[('LECTURER', 'Lecturer'), ('ASSISTANT', 'Assistant')], max_length=9)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elnure_core.instructor')),
                ('to_elective_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elnure_core.electivecourse')),
            ],
            options={
                'db_table': 'instructor_assignment',
            },
        ),
        migrations.CreateModel(
            name='ElectiveGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('elective_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='elnure_core.electivecourse')),
            ],
            options={
                'db_table': 'elective_groups',
            },
        ),
        migrations.AddField(
            model_name='electivecourse',
            name='instructors',
            field=models.ManyToManyField(related_name='assigned_courses', through='elnure_core.InstructorAssignment', to='elnure_core.instructor'),
        ),
        migrations.AddField(
            model_name='electivecourse',
            name='semester',
            field=models.ForeignKey(help_text='Semester of elective course', on_delete=django.db.models.deletion.RESTRICT, related_name='elective_courses', to='elnure_config.semester'),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('value', models.JSONField(help_text='Value to be processed in one of the descendants of BaseChoiceStrategy')),
                ('strategy', elnure_common.fields.ElnureEnumField(choices=[('DEFAULT', 'Default'), ('OPTIMIZED', 'Optimized')], max_length=9, null=True)),
                ('application_window', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='choices', to='elnure_config.applicationwindow')),
                ('elective_groups', models.ManyToManyField(help_text='Elective groups attached to students after groups formation', related_name='students_choices', to='elnure_core.electivegroup')),
                ('semester', models.ForeignKey(help_text='Semester of elective courses which student applies for', on_delete=django.db.models.deletion.RESTRICT, related_name='choices', to='elnure_config.semester')),
            ],
            options={
                'db_table': 'choices',
            },
        ),
    ]
