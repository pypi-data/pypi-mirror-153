from django.forms.widgets import MultiWidget, Select, Widget

from opening_hours_management.models import OpeningHours


class SelectTimeWidget(MultiWidget):
    template_name = "opening_hours_management/widgets/selecttime.html"

    def __init__(self, attrs=None):
        hours_choices = [(h, h) for h in range(24)]
        minutes_choices = [(m, m) for m in range(0, 60, 5)]
        widgets = (
            Select(attrs=attrs, choices=hours_choices),
            Select(attrs=attrs, choices=minutes_choices),
        )
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            return [value.hour, value.minute]
        return [None, None]


class DisabledSelectWidget(Select):
    template_name = "opening_hours_management/widgets/disabledselect.html"

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.update({"disabled": "disabled"})
        return super().__init__(attrs)


class OpeningHoursWidget(Widget):
    template_name = "opening_hours_management/widgets/opening_hours_widget.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["type"] = "hidden"
        if value:
            opening_hours = OpeningHours.objects.get(pk=value)
            context["widget"]["instance"] = opening_hours
        return context

    class Media:
        js = ["admin/js/RelatedOpeningHoursLookups.js"]
