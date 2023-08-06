from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from .fieldsets import get_phq9_fieldsets


def get_phq9_radio_fields() -> dict:
    return {
        # "crf_status": admin.VERTICAL,
        "ph9appetit": admin.VERTICAL,
        "ph9badabt": admin.VERTICAL,
        "ph9concen": admin.VERTICAL,
        "ph9feel": admin.VERTICAL,
        "ph9functio": admin.VERTICAL,
        "ph9interst": admin.VERTICAL,
        "ph9moving": admin.VERTICAL,
        "ph9tired": admin.VERTICAL,
        "ph9troubl": admin.VERTICAL,
        "ph9though": admin.VERTICAL,
    }


class Phq9ModelAdminMixin:
    form = None  # PatientHealthForm

    fieldsets = (
        get_phq9_fieldsets(),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = get_phq9_radio_fields()
