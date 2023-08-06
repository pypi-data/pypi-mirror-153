from django import forms
from django.conf import settings
from edc_constants.constants import NO, YES
from edc_crf.forms import CrfFormValidatorMixin
from edc_form_validators import FormValidatorMixin
from edc_form_validators.form_validator import FormValidator
from edc_visit_schedule.utils import raise_if_not_baseline

from edc_phq9.fieldsets import get_phq9_fields

from .utils import get_phq9_model_cls


class Phq9FormValidatorMixin:
    def clean_phq9(self):
        if getattr(settings, "EDC_PHQ9_MODEL_AT_BASELINE_ONLY", True):
            raise_if_not_baseline(self.cleaned_data.get("subject_visit"))
        self.required_if(NO, field="ph9_performed", field_required="ph9_not_performed_reason")
        for fld in get_phq9_fields():
            self.applicable_if(YES, field="ph9_performed", field_applicable=fld)


class Phq9FormValidator(Phq9FormValidatorMixin, CrfFormValidatorMixin, FormValidator):
    def clean(self):
        self.clean_phq9()


class Phq9Form(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = Phq9FormValidator

    class Meta:
        model = get_phq9_model_cls()
        fields = "__all__"
