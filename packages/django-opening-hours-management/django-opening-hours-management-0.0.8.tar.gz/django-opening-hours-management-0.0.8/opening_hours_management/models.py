from django.core.exceptions import ValidationError
from django.db import models
from django.utils import formats
from django.utils.translation import ugettext_lazy as _

from .conf import settings as local_settings
from .constants import MIDNIGHT_TIME
from .shortcuts import format_time_range

# Create your models here.

ISO_WEEKDAY_CHOICES = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


class TimeRange(models.Model):
    opening_time = models.TimeField(_("Opening time"), null=True, blank=True)
    closing_time = models.TimeField(_("Closing time"), null=True, blank=True)

    class Meta:
        abstract = True
        # WARNING: Never remove this ordering key
        ordering = ["opening_time"]

    @property
    def range_display(self):
        return format_time_range(self.opening_time, self.closing_time)

    def __str__(self):
        return self.range_display

    def clean(self):
        if self.opening_time is not None and self.closing_time is not None:
            # Specific case for closing time at midnight
            if self.closing_time != MIDNIGHT_TIME:
                if self.opening_time > self.closing_time:
                    raise ValidationError(
                        {
                            "opening_time": _(
                                "The opening time cannot be later than the closing time"
                            )
                        }
                    )

                if self.opening_time == self.closing_time:
                    raise ValidationError(
                        {"opening_time": _("The start and end times cannot be equal")}
                    )


class OpeningHours(models.Model):
    always_open = models.BooleanField(
        _("Open 24/7"),
        default=False,
        db_index=True,
        help_text=_("If checked, prevails on week day values"),
    )

    class Meta:
        verbose_name = _("Opening hours")
        verbose_name_plural = _("Openings hours")
        app_label = "opening_hours_management"

    def __str__(self):
        opening_char = "✓" if self.always_open else "✗"
        return f"{self._meta.verbose_name} #{self.pk} - {opening_char}open 24/7"


class WeekDayHours(models.Model):
    opening_hours = models.ForeignKey(
        OpeningHours,
        verbose_name=_("Opening hours"),
        on_delete=models.CASCADE,
        related_name="weekday_hours",
    )

    week_day = models.PositiveSmallIntegerField(
        _("Week day"), choices=ISO_WEEKDAY_CHOICES
    )

    closed = models.BooleanField(
        _("Closed"),
        default=False,
        help_text=_("If checked, prevails on time range values"),
    )

    class Meta:
        verbose_name = _("Week day hours")
        verbose_name_plural = _("Week days hours")
        app_label = "opening_hours_management"
        unique_together = ["opening_hours", "week_day"]
        # WARNING: Never remove this ordering key
        ordering = ["week_day"]

    def __str__(self):
        opening_status = _("Closed") if self.closed else _("Open")
        return f"{self.get_week_day_display()} - {opening_status}"


class WeekDayTimeRange(TimeRange):
    week_day_hours = models.ForeignKey(
        WeekDayHours,
        verbose_name=_("Week day hours"),
        on_delete=models.CASCADE,
        related_name="weekday_time_ranges",
    )

    class Meta(TimeRange.Meta):
        verbose_name = _("Week day time range")
        verbose_name_plural = _("Week days time ranges")
        app_label = "opening_hours_management"

    def __str__(self):
        hours_range_str = super().__str__()
        return f"{self.week_day_hours} - {hours_range_str}"


class GeneralHolidaysHours(models.Model):
    opening_hours = models.OneToOneField(
        OpeningHours,
        verbose_name=_("Opening hours"),
        on_delete=models.CASCADE,
        related_name="general_holidays_hours",
    )

    closed = models.BooleanField(
        _("Closed"),
        default=False,
        help_text=_("If checked, prevails on time range values"),
    )

    class Meta:
        verbose_name = _("General holidays hours")
        verbose_name_plural = _("General holidays hours")
        app_label = "opening_hours_management"

    def __str__(self):
        if self.closed:
            opening_status = _("Closed")
        elif self.general_holidays_time_ranges.count() > 0:
            opening_status = _("Open")
        else:
            opening_status = _("undefined")

        return f"{opening_status}"


class GeneralHolidaysTimeRange(TimeRange):
    general_holidays_hours = models.ForeignKey(
        GeneralHolidaysHours,
        verbose_name=_("General holidays hours"),
        on_delete=models.CASCADE,
        related_name="general_holidays_time_ranges",
    )

    class Meta(TimeRange.Meta):
        verbose_name = _("General holidays time range")
        verbose_name_plural = _("General holidays time range")
        app_label = "opening_hours_management"

    def __str__(self):
        hours_range_str = super().__str__()
        return f"{self.general_holidays_hours} - {hours_range_str}"


class SpecificPeriodHours(models.Model):
    opening_hours = models.ForeignKey(
        OpeningHours,
        verbose_name=_("Opening hours"),
        on_delete=models.CASCADE,
        related_name="specific_period_hours",
    )

    from_date = models.DateField(_("From"), db_index=True)
    to_date = models.DateField(_("To"), db_index=True)

    closed = models.BooleanField(
        _("Closed"),
        default=False,
        help_text=_("If checked, prevails on time range values"),
    )

    closure_reason = models.PositiveSmallIntegerField(
        _("Closure reason"),
        choices=local_settings.CLOSURE_CAUSE_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Specific period hours")
        verbose_name_plural = _("Specific periods hours")
        app_label = "opening_hours_management"
        # WARNING: Never remove this ordering key
        ordering = ["from_date"]

    def __str__(self):
        if self.closed:
            opening_status = (
                _("Closed")
                if self.closure_reason is None
                else self.get_closure_reason_display()
            )
        else:
            opening_status = _("Open")

        return f"{self.from_date} - {self.to_date} - {opening_status}"

    @property
    def period_display(self):
        from_date_format = formats.date_format(self.from_date, "SHORT_DATE_FORMAT")
        to_date_format = formats.date_format(self.to_date, "SHORT_DATE_FORMAT")
        if self.from_date == self.to_date:
            return from_date_format
        else:
            return f"{from_date_format} - {to_date_format}"

    def clean(self):
        if self.from_date is not None and self.to_date is not None:
            if self.from_date > self.to_date:
                raise ValidationError(
                    {"to_date": _("The start date cannot be later than the end date")}
                )

        if self.closed is not True and self.closure_reason is not None:
            raise ValidationError(
                {
                    "closure_reason": _(
                        'Closure reason is used only if the field "Closed" is checked'
                    )
                }
            )


class SpecificPeriodTimeRange(TimeRange):
    specific_period_hours = models.ForeignKey(
        SpecificPeriodHours,
        verbose_name=_("Specific period hours"),
        on_delete=models.CASCADE,
        related_name="specific_period_time_ranges",
    )

    class Meta(TimeRange.Meta):
        verbose_name = _("Specific period time range")
        verbose_name_plural = _("Specific periods times ranges")
        app_label = "opening_hours_management"

    def __str__(self):
        hours_range_str = super().__str__()
        return f"{self.specific_period_hours} - {hours_range_str}"
