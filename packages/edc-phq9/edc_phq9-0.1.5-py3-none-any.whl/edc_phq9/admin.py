from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin import SimpleHistoryAdmin

from .admin_site import edc_phq9_admin
from .fieldsets import get_phq9_fieldsets
from .forms import Phq9Form
from .model_admin_mixins import Phq9ModelAdminMixin
from .models import Phq9


def get_fieldsets() -> tuple:
    fieldset = (
        None,
        {
            "fields": (
                "subject_identifier",
                "report_datetime",
                "ph9_performed",
                "ph9_not_performed_reason",
            )
        },
    )

    fieldsets = (fieldset,) + (get_phq9_fieldsets(),)
    fieldsets += (audit_fieldset_tuple,)
    return fieldsets


@admin.register(Phq9, site=edc_phq9_admin)
class Phq9Admin(
    Phq9ModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = Phq9Form

    fieldsets = get_fieldsets()
