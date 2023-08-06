from datetime import date, datetime, time
from time import mktime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .widgets import SelectTimeWidget


class FormTimeField(forms.TimeField):
    widget = SelectTimeWidget

    def bound_data(self, data, initial):
        bound_data = super().bound_data(data, initial)

        if isinstance(bound_data, list):
            hour, minute = map(lambda x: int(x) if x else None, bound_data)
            if not None in [hour, minute]:
                return time(hour, minute, 0)
            else:
                return None
        else:
            return bound_data

    def to_python(self, value):
        """
        Validate that the input can be converted to a time. Return a Python
        datetime.time object.
        """
        hour, minute = map(lambda x: int(x) if x else None, value)

        if not None in [hour, minute]:
            return time(hour, minute, 0)
        else:
            return None


class TimeStampField(forms.Field):
    default_error_messages = {
        "invalid": _("Enter a valid date/time."),
    }

    def prepare_value(self, value):
        if isinstance(value, (date, datetime)):
            if isinstance(value, date):
                min_time = datetime.min.time()
                value_dt = datetime.combine(value, min_time)
            else:
                value_dt = value

            value_timestamp = mktime(value_dt.timetuple())
            return value_timestamp
        return value

    def to_python(self, value):
        if value in self.empty_values:
            return None

        if isinstance(value, (date, datetime)):
            return value
        else:
            try:
                value_dt = datetime.fromtimestamp(int(float(value)))
                return value_dt.date() if self.as_date else value_dt
            except (ValueError, TypeError):
                pass

        raise ValidationError(self.error_messages["invalid"], code="invalid")


class TimeStampDatetimeField(TimeStampField):
    as_date = False


class TimeStampDateField(TimeStampField):
    as_date = True
