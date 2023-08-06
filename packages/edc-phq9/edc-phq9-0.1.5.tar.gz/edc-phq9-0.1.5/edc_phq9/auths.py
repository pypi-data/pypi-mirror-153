from edc_auth.site_auths import site_auths

from .auth_objects import PHQ9, PHQ9_SUPER, PHQ9_VIEW, phq9_codenames

site_auths.add_group(*phq9_codenames, name=PHQ9_VIEW, view_only=True)
site_auths.add_group(*phq9_codenames, name=PHQ9, no_delete=True)
site_auths.add_group(*phq9_codenames, name=PHQ9_SUPER)
