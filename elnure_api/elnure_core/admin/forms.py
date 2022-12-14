import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from elnure_common.json_schema import validate_schema, DefaultStrategySchemas
from elnure_core import models


class BlockForm(forms.ModelForm):
    must_choose = forms.CharField(
        help_text=_(
            "Number of coureses to choose for this block or asterisk(*) to choose all"
        ),
        validators=[
            RegexValidator(
                r"(\*|\d+)", _("Must choose should be either asterisk(*) or a number.")
            ),
        ],
    )
    elective_courses = forms.ModelMultipleChoiceField(
        models.ElectiveCourse.objects.all(), required=False
    )

    ALL_COURSES = "*"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial["elective_courses"] = self.instance.elective_courses.all()

            if len(self.initial["elective_courses"]) == self.instance.must_choose:
                self.initial["must_choose"] = self.ALL_COURSES
            elif self.instance.must_choose:
                self.initial["must_choose"] = self.instance.must_choose

    def clean(self):
        must_choose = self.cleaned_data.get("must_choose")
        elective_courses = self.cleaned_data.get("elective_courses")
        total_credits = self.cleaned_data.get("total_credits")

        elective_course_credits = 0
        if must_choose == self.ALL_COURSES:
            self.cleaned_data["must_choose"] = len(elective_courses)

            for elective_course in elective_courses:
                elective_course_credits += elective_course.credits
        elif must_choose:
            self.cleaned_data["must_choose"] = int(must_choose)

            if int(must_choose) > len(elective_courses):
                raise ValidationError(
                    _(
                        "Block's number of courses to choose should not be higher than actual number of elective courses."
                    )
                )

            distinct_credits = set(
                elective_course.credits for elective_course in elective_courses
            )
            if len(distinct_credits) != 1:
                raise ValidationError(
                    _(
                        "Credits should be equal in each elecitve course when must_choose='*'."
                    )
                )

            credits = distinct_credits.pop()
            elective_course_credits = credits * int(must_choose)

        if total_credits != elective_course_credits:
            raise ValidationError(
                _(
                    "Total block credits must be equal to sum of credits for elective courses."
                )
            )

    def _save_m2m(self):
        if "elective_courses" in self.changed_data:
            self.instance.elective_courses.set(self.cleaned_data["elective_courses"])
        return super()._save_m2m()


class ElectiveGroupStudentAssociationInlineForm(forms.ModelForm):
    def clean(self):
        if "elective_group" in self.changed_data or "student" in self.changed_data:
            elective_group = self.cleaned_data["elective_group"]
            student = self.cleaned_data["student"]

            current_block = elective_group.elective_course.block
            if not current_block:
                raise ValidationError(
                    _(
                        f"Elective course '{elective_group.elective_course.shortcut}' does not have an assigned block. Please assign a block and repeat."
                    )
                )
            semester_id = elective_group.elective_course.block.semester_id

            blocks = models.Block.objects.filter(semester_id=semester_id)

            expected_num_of_groups = sum(block.must_choose for block in blocks)
            current_num_of_groups = student.elective_groups.filter(
                elective_course__block__semester_id=semester_id
            ).count()

            if current_num_of_groups == expected_num_of_groups:
                raise ValidationError(
                    _(
                        f"Student already enrolled in maximum number of elective groups for the semester {semester_id}"
                    )
                )


class RunSnapshotForm(forms.ModelForm):
    def clean(self):
        application_window = self.cleaned_data.get("application_window")
        status = self.cleaned_data["status"]
        need_redistribution = self.cleaned_data.get("need_redistribution", {})
        result = self.cleaned_data.get("result", {})

        if status == models.RunSnapshot.Status.ACCEPTED and application_window:
            accepted_snapshots = models.RunSnapshot.objects.filter(
                application_window=application_window, status=status
            )

            if self.instance.id:
                accepted_snapshots = accepted_snapshots.exclude(id=self.instance.id)

            already_exists = accepted_snapshots.exists()
            if already_exists:
                raise ValidationError(
                    _("Snapshot is already accepted for this application window.")
                )

        validate_schema(
            need_redistribution,
            DefaultStrategySchemas.NEED_REDISTRIBUTION,
            exc_cls=ValidationError,
            exc_msg=_(
                f"need_redistribution has incorrect structure. Schema: {DefaultStrategySchemas.NEED_REDISTRIBUTION}"
            ),
        )

        validate_schema(
            result,
            DefaultStrategySchemas.RESULT,
            exc_cls=ValidationError,
            exc_msg=_(
                f"result has incorrect structure. Schema: {DefaultStrategySchemas.RESULT}"
            ),
        )
