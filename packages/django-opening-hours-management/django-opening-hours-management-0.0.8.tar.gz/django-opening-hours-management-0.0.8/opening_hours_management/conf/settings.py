from django.conf import settings
from django.utils.translation import ugettext_lazy as _

CUSTOM_ADMIN_RELATED_FIELD = getattr(
    settings, "DJANGO_OPENING_HOURS_MANAGEMENT_CUSTOM_ADMIN_RELATED", False
)

CLOSURE_CAUSE_CHOICES = getattr(
    settings,
    "DJANGO_OPENING_HOURS_MANAGEMENT_CLOSURE_CAUSE_CHOICES",
    [(1, _("Closed"))],
)
