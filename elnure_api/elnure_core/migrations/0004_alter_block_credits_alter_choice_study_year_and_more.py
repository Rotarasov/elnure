# Generated by Django 4.0.4 on 2022-05-22 21:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elnure_core", "0003_alter_choice_study_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="credits",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="choice",
            name="study_year",
            field=models.IntegerField(
                help_text="Study year of elective courses which student applies for",
                validators=[
                    django.core.validators.MinValueValidator(2),
                    django.core.validators.MaxValueValidator(4),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="electivecourse",
            name="capacity",
            field=models.IntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="electivecourse",
            name="credits",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="electivecourse",
            name="semester",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(8),
                ]
            ),
        ),
    ]