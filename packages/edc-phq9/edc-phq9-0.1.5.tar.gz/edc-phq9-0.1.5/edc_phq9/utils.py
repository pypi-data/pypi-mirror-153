from django.apps import apps as django_apps
from django.conf import settings
from django.db import models

# don't delete. so attr is searchable
EDC_PHQ9_MODEL = "EDC_PHQ9_MODEL"


def get_phq9_model_name() -> str:
    return getattr(settings, "EDC_PHQ9_MODEL", "edc_phq9.phq9")


def get_phq9_model_cls() -> models.Model:
    return django_apps.get_model(get_phq9_model_name())
