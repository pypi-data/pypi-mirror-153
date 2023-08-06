import json

import nested_admin
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from opening_hours_management.templatetags.opening_hours_management import (
    show_opening_hours,
)

from .conf import settings as local_settings
from .forms import (
    GeneralHolidaysHoursInlineFormSet,
    GeneralHolidaysTimeRangeInlineFormSet,
    GeneralHolidaysTimeRangeModelForm,
    SpecificPeriodHoursInlineFormSet,
    SpecificPeriodTimeRangeInlineFormSet,
    SpecificPeriodTimeRangeModelForm,
    WeekDayHoursInlineFormSet,
    WeekDayTimeRangeInlineFormSet,
    WeekDayTimeRangeModelForm,
)
from .models import (
    GeneralHolidaysHours,
    GeneralHolidaysTimeRange,
    OpeningHours,
    SpecificPeriodHours,
    SpecificPeriodTimeRange,
    WeekDayHours,
    WeekDayTimeRange,
)
from .widgets import DisabledSelectWidget


class WeekDayTimeRangeInline(nested_admin.NestedTabularInline):
    model = WeekDayTimeRange
    formset = WeekDayTimeRangeInlineFormSet
    form = WeekDayTimeRangeModelForm
    extra = 0


class WeekDayHoursInline(nested_admin.NestedStackedInline):
    formset = WeekDayHoursInlineFormSet
    model = WeekDayHours
    inlines = [WeekDayTimeRangeInline]
    max_num = 7
    extra = 7

    def has_delete_permission(self, request, obj=None):
        return False

    def get_formset(self, request, obj=None, **kwargs):
        kwargs["widgets"] = {"week_day": DisabledSelectWidget}
        return super().get_formset(request, obj, **kwargs)


class GeneralHolidaysTimeRangeInline(nested_admin.NestedTabularInline):
    model = GeneralHolidaysTimeRange
    formset = GeneralHolidaysTimeRangeInlineFormSet
    form = GeneralHolidaysTimeRangeModelForm
    extra = 0


class GeneralHolidaysHoursInline(nested_admin.NestedStackedInline):
    formset = GeneralHolidaysHoursInlineFormSet
    model = GeneralHolidaysHours
    inlines = [GeneralHolidaysTimeRangeInline]
    max_num = 1
    extra = 1

    def has_delete_permission(self, request, obj=None):
        return False


class SpecificPeriodTimeRangeInline(nested_admin.NestedTabularInline):
    model = SpecificPeriodTimeRange
    formset = SpecificPeriodTimeRangeInlineFormSet
    form = SpecificPeriodTimeRangeModelForm
    extra = 0


class SpecificPeriodHoursInline(nested_admin.NestedStackedInline):
    formset = SpecificPeriodHoursInlineFormSet
    inlines = [SpecificPeriodTimeRangeInline]
    model = SpecificPeriodHours
    extra = 0


class OpeningHoursAdmin(nested_admin.NestedModelAdmin):
    model = OpeningHours
    inlines = (
        WeekDayHoursInline,
        GeneralHolidaysHoursInline,
        SpecificPeriodHoursInline,
    )
    popup_response_template = (
        "opening_hours_management/admin/openinghours/popup_response.html"
        if local_settings.CUSTOM_ADMIN_RELATED_FIELD
        else None
    )

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determine the HttpResponse for the add_view stage.
        """

        if IS_POPUP_VAR in request.POST:
            opts = obj._meta

            to_field = request.POST.get(TO_FIELD_VAR)
            if to_field:
                attr = str(to_field)
            else:
                attr = obj._meta.pk.attname
            value = obj.serializable_value(attr)
            opening_hours_display = render_to_string(
                "opening_hours_management/templatetags/opening_hours.html",
                show_opening_hours(obj),
            )
            popup_response_data = json.dumps(
                {
                    "value": str(value),
                    "obj": str(obj),
                    "obj_display": str(opening_hours_display),
                }
            )
            return TemplateResponse(
                request,
                self.popup_response_template
                or [
                    "admin/%s/%s/popup_response.html"
                    % (opts.app_label, opts.model_name),
                    "admin/%s/popup_response.html" % opts.app_label,
                    "admin/popup_response.html",
                ],
                {"popup_response_data": popup_response_data},
            )

        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        """
        Determine the HttpResponse for the change_view stage.
        """

        if IS_POPUP_VAR in request.POST:
            opts = obj._meta
            to_field = request.POST.get(TO_FIELD_VAR)
            attr = str(to_field) if to_field else opts.pk.attname
            value = request.resolver_match.kwargs["object_id"]
            new_value = obj.serializable_value(attr)
            opening_hours_display = render_to_string(
                "opening_hours_management/templatetags/opening_hours.html",
                show_opening_hours(obj),
            )
            popup_response_data = json.dumps(
                {
                    "action": "change",
                    "value": str(value),
                    "obj": str(obj),
                    "obj_display": str(opening_hours_display),
                    "new_value": str(new_value),
                }
            )
            return TemplateResponse(
                request,
                self.popup_response_template
                or [
                    "admin/%s/%s/popup_response.html"
                    % (opts.app_label, opts.model_name),
                    "admin/%s/popup_response.html" % opts.app_label,
                    "admin/popup_response.html",
                ],
                {"popup_response_data": popup_response_data},
            )

        return super().response_change(request, obj)


admin.site.register(OpeningHours, OpeningHoursAdmin)
