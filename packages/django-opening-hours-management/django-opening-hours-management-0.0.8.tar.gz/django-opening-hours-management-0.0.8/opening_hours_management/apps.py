from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OpeningHoursManagementConfig(AppConfig):
    label = "opening_hours_management"
    name = "opening_hours_management"
    verbose_name = _("Opening hours management")
