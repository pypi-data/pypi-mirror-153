from django import template
from django.conf import settings
from django.db.models import Prefetch, prefetch_related_objects
from django.utils.timezone import localtime, now

from opening_hours_management.models import (
    GeneralHolidaysHours,
    SpecificPeriodHours,
    WeekDayHours,
)

register = template.Library()


@register.inclusion_tag("opening_hours_management/templatetags/opening_hours.html")
def show_opening_hours(instance, show_passed_specific_period_hours=False):
    specific_period_hours_qs = SpecificPeriodHours.objects.all()

    if show_passed_specific_period_hours is False:
        now_dt = now()
        if settings.USE_TZ:
            now_dt = localtime(now_dt)
        now_date = now_dt.date()

        specific_period_hours_qs = specific_period_hours_qs.filter(
            to_date__gte=now_date
        )

    prefetch_related_objects(
        [instance],
        Prefetch(
            "weekday_hours",
            queryset=WeekDayHours.objects.all().prefetch_related("weekday_time_ranges"),
        ),
        Prefetch(
            "general_holidays_hours",
            queryset=GeneralHolidaysHours.objects.all().prefetch_related(
                "general_holidays_time_ranges"
            ),
        ),
        Prefetch(
            "specific_period_hours",
            queryset=specific_period_hours_qs.prefetch_related(
                "specific_period_time_ranges"
            ),
        ),
    )

    try:
        general_holidays_hours = instance.general_holidays_hours
    except GeneralHolidaysHours.DoesNotExist:
        general_holidays_hours = None

    return {
        "instance": instance,
        "weekday_hours": instance.weekday_hours.all(),
        "general_holidays_hours": general_holidays_hours,
        "specific_period_hours": instance.specific_period_hours.all(),
    }
