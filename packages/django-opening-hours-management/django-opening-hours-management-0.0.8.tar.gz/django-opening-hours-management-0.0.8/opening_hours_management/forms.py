from datetime import datetime, time

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.forms.models import modelformset_factory
from django.utils import formats
from django.utils.translation import ugettext_lazy as _
from intervaltree import Interval, IntervalTree

from .constants import MIDNIGHT_TIME
from .fields import FormTimeField, TimeStampDateField
from .models import (
    ISO_WEEKDAY_CHOICES,
    GeneralHolidaysHours,
    GeneralHolidaysTimeRange,
    OpeningHours,
    SpecificPeriodHours,
    SpecificPeriodTimeRange,
    WeekDayHours,
    WeekDayTimeRange,
)
from .shortcuts import format_time_range, time_total_seconds


class OpeningHoursModelForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ["always_open"]


class TimeRangeModelForm(forms.ModelForm):
    opening_time = FormTimeField()
    closing_time = FormTimeField()


class TimeRangeInlineFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        super().clean()

        forms_to_delete = self.deleted_forms
        valid_forms = [
            form
            for form in self.forms
            if form.is_valid() and form not in forms_to_delete
        ]

        interval_tree = IntervalTree()

        has_concurrent_periods = False
        for form in valid_forms:
            opening_time = form.cleaned_data.get("opening_time")
            closing_time = form.cleaned_data.get("closing_time")

            if opening_time is not None and closing_time is not None:
                opening_time = time_total_seconds(opening_time)

                if closing_time == MIDNIGHT_TIME:
                    closing_time = time_total_seconds(time(23, 59)) + 1
                else:
                    closing_time = time_total_seconds(closing_time)

                overlap_set = interval_tree.overlap(opening_time, closing_time)

                if len(overlap_set) > 0:
                    overlap = list(overlap_set)[0]
                    overlap_form_data = overlap.data.cleaned_data
                    overlap_opening_time = overlap_form_data["opening_time"]
                    overlap_closing_time = overlap_form_data["closing_time"]
                    overlap_display = format_time_range(
                        overlap_opening_time, overlap_closing_time
                    )

                    form.add_error(
                        "opening_time",
                        _(
                            "This period is in conflict with the period {overlap_display}"
                        ).format(overlap_display=overlap_display),
                    )
                    has_concurrent_periods = True

                interval = Interval(opening_time, closing_time, form)
                interval_tree.add(interval)

        if has_concurrent_periods:
            raise ValidationError(
                _("The form cannot be validated because some periods are in conflict")
            )


class WeekDayTimeRangeModelForm(TimeRangeModelForm):
    class Meta:
        model = WeekDayTimeRange
        exclude = []


class WeekDayTimeRangeInlineFormSet(TimeRangeInlineFormSet):
    pass


class WeekDayHoursModelForm(forms.ModelForm):
    class Meta:
        model = WeekDayHours
        exclude = []


class WeekDayHoursInlineFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        # Initialize week days only if no data is provided, otherwise no changes are detected on sub-forms save
        initial = (
            [{"week_day": weekday[0]} for weekday in ISO_WEEKDAY_CHOICES]
            if "data" not in kwargs
            else None
        )
        super().__init__(initial=initial, *args, **kwargs)


class GeneralHolidaysTimeRangeModelForm(TimeRangeModelForm):
    class Meta:
        model = GeneralHolidaysTimeRange
        exclude = []


class GeneralHolidaysTimeRangeInlineFormSet(TimeRangeInlineFormSet):
    pass


class GeneralHolidaysHoursInlineFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        initial = [{"closed": True}] if "data" not in kwargs else None
        super().__init__(initial=initial, *args, **kwargs)


class GeneralHolidaysHoursModelForm(forms.ModelForm):
    class Meta:
        model = GeneralHolidaysHours
        exclude = []


class SpecificPeriodTimeRangeModelForm(TimeRangeModelForm):
    class Meta:
        model = SpecificPeriodTimeRange
        exclude = []


class SpecificPeriodTimeRangeInlineFormSet(TimeRangeInlineFormSet):
    pass


class SpecificPeriodHoursModelForm(forms.ModelForm):
    from_date = TimeStampDateField()
    to_date = TimeStampDateField()

    class Meta:
        model = SpecificPeriodHours
        fields = ["from_date", "to_date", "closed", "closure_reason"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ["from_date", "to_date"]:
            base_field = SpecificPeriodHours._meta.get_field(field).formfield()

            for attr in ["required", "label", "help_text"]:
                setattr(self.fields[field], attr, getattr(base_field, attr))


class SpecificPeriodHoursInlineFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        super().clean()

        forms_to_delete = self.deleted_forms
        valid_forms = [
            form
            for form in self.forms
            if form.is_valid() and form not in forms_to_delete
        ]

        interval_tree = IntervalTree()

        has_concurrent_periods = False
        for form in valid_forms:
            if "from_date" in form.cleaned_data and "to_date" in form.cleaned_data:
                from_timestamp = datetime.combine(
                    form.cleaned_data["from_date"], datetime.min.time()
                ).timestamp()
                to_timestamp = datetime.combine(
                    form.cleaned_data["to_date"], datetime.max.time()
                ).timestamp()

                overlap_set = interval_tree.overlap(from_timestamp, to_timestamp)

                if len(overlap_set) > 0:
                    overlap = list(overlap_set)[0]
                    overlap_form_data = overlap.data.cleaned_data
                    overlap_from = overlap_form_data["from_date"]
                    overlap_to = overlap_form_data["to_date"]
                    overlap_from = formats.date_format(overlap_from, "DATE_FORMAT")
                    overlap_to = formats.date_format(overlap_to, "DATE_FORMAT")
                    overlap_display = f"{overlap_from} - {overlap_to}"
                    form.add_error(
                        "from_date",
                        _(
                            "This period is in conflict with the period {overlap_display}"
                        ).format(overlap_display=overlap_display),
                    )
                    has_concurrent_periods = True

                interval = Interval(from_timestamp, to_timestamp, form)
                interval_tree.add(interval)

        if has_concurrent_periods:
            raise ValidationError(
                _("The form cannot be validated because some periods are in conflict")
            )


WeekDayHoursFormSet = inlineformset_factory(
    OpeningHours,
    WeekDayHours,
    form=WeekDayHoursModelForm,
    formset=WeekDayHoursInlineFormSet,
    can_delete=True,
    extra=7,
    max_num=7,
)


WeekDayHoursTimeRangeFormSet = inlineformset_factory(
    WeekDayHours,
    WeekDayTimeRange,
    form=WeekDayTimeRangeModelForm,
    formset=WeekDayTimeRangeInlineFormSet,
    can_delete=True,
    extra=0,
)

GeneralHolidaysTimeRangeFormSet = inlineformset_factory(
    GeneralHolidaysHours,
    GeneralHolidaysTimeRange,
    form=GeneralHolidaysTimeRangeModelForm,
    formset=GeneralHolidaysTimeRangeInlineFormSet,
    can_delete=True,
    extra=0,
)


SpecificPeriodHoursFormSet = inlineformset_factory(
    OpeningHours,
    SpecificPeriodHours,
    form=SpecificPeriodHoursModelForm,
    formset=SpecificPeriodHoursInlineFormSet,
    can_delete=True,
    extra=0,
)

SpecificPeriodTimeRangeFormSet = inlineformset_factory(
    SpecificPeriodHours,
    SpecificPeriodTimeRange,
    form=SpecificPeriodTimeRangeModelForm,
    formset=SpecificPeriodTimeRangeInlineFormSet,
    can_delete=True,
    extra=0,
)
