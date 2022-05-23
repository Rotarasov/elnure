# Generated by Django 4.0.4 on 2022-05-23 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elnure_users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ratings",
            field=models.JSONField(
                default=[],
                help_text="Student rating for multiple semesters ordered by semester",
            ),
        ),
    ]