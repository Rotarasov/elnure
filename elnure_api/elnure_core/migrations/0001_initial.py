# Generated by Django 4.0.2 on 2022-02-14 22:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import elnure_common.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplicationWindow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
            ],
            options={
                "db_table": "application_windows",
            },
        ),
        migrations.CreateModel(
            name="Block",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
                ("credits", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "blocks",
            },
        ),
        migrations.CreateModel(
            name="ElectiveCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "semester",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(8)]
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("shortcut", models.CharField(max_length=10)),
                ("syllabus", models.CharField(max_length=300)),
                ("capacity", models.PositiveIntegerField(null=True)),
                ("credits", models.PositiveIntegerField()),
                (
                    "performance_assessment",
                    elnure_common.fields.ElnureEnumField(
                        choices=[
                            ("SESSION_EXAMINATION", "Session Examination"),
                            ("GRADED_SEMESTER", "Graded Semester"),
                        ],
                        default="GRADED_SEMESTER",
                        max_length=19,
                    ),
                ),
                (
                    "block",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="courses",
                        to="elnure_core.block",
                    ),
                ),
            ],
            options={
                "db_table": "elective_courses",
            },
        ),
        migrations.CreateModel(
            name="Instructor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(max_length=150)),
            ],
            options={
                "db_table": "instructors",
            },
        ),
        migrations.CreateModel(
            name="InstructorAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "position",
                    elnure_common.fields.ElnureEnumField(
                        choices=[("LECTURER", "Lecturer"), ("ASSISTANT", "Assistant")],
                        max_length=9,
                    ),
                ),
                (
                    "instructor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elnure_core.instructor",
                    ),
                ),
                (
                    "to_elective_course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elnure_core.electivecourse",
                    ),
                ),
            ],
            options={
                "db_table": "instructor_assignment",
            },
        ),
        migrations.CreateModel(
            name="ElectiveGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=30)),
                (
                    "elective_course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="groups",
                        to="elnure_core.electivecourse",
                    ),
                ),
            ],
            options={
                "db_table": "elective_groups",
            },
        ),
        migrations.AddField(
            model_name="electivecourse",
            name="instructors",
            field=models.ManyToManyField(
                related_name="assigned_courses",
                through="elnure_core.InstructorAssignment",
                to="elnure_core.Instructor",
            ),
        ),
        migrations.CreateModel(
            name="Choice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "study_year",
                    models.PositiveIntegerField(
                        help_text="Study year of elective courses which student applies for",
                        validators=[django.core.validators.MaxValueValidator(4)],
                    ),
                ),
                (
                    "value",
                    models.JSONField(
                        help_text="Value to be processed in one of the descendants of BaseChoiceHandler"
                    ),
                ),
                (
                    "elective_groups",
                    models.ManyToManyField(
                        related_name="students_choices", to="elnure_core.ElectiveGroup"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="elective_course_choices",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "choices",
            },
        ),
    ]
