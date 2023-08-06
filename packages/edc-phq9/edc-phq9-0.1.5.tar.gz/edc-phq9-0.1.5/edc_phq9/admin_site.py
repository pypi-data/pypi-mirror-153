from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

edc_phq9_admin = EdcAdminSite(name="edc_phq9_admin", app_label=AppConfig.name)
