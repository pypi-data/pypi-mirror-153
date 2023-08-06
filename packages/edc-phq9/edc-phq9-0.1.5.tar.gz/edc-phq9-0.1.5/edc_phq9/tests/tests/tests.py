from django.test import TestCase
from edc_constants.constants import NO, YES
from edc_utils import get_utcnow

from edc_phq9.constants import NEARLY_EVERYDAY
from edc_phq9.fieldsets import get_phq9_fields
from edc_phq9.forms import Phq9Form
from edc_phq9.utils import get_phq9_model_cls


class Phq9Tests(TestCase):
    def test_model(self):
        get_phq9_model_cls()

    def test_form(self):
        form = Phq9Form(data={})
        form.is_valid()
        self.assertIn("subject_identifier", form._errors)

    def test_form_performed(self):
        data = {fld: NEARLY_EVERYDAY for fld in get_phq9_fields()}
        data.update(
            subject_identifier="12345", report_datetime=get_utcnow(), ph9_performed=YES
        )
        form = Phq9Form(data=data)
        form.is_valid()
        self.assertEqual(form._errors, {})

    def test_form_not_performed(self):
        data = {fld: NEARLY_EVERYDAY for fld in get_phq9_fields()}
        data.update(subject_identifier="12345", report_datetime=get_utcnow(), ph9_performed=NO)
        form = Phq9Form(data=data)
        form.is_valid()
        self.assertIn("ph9_not_performed_reason", form._errors)
        data.update(ph9_not_performed_reason="blah blah")
        form = Phq9Form(data=data)
        form.is_valid()
        self.assertIn("ph9interst", form._errors)
