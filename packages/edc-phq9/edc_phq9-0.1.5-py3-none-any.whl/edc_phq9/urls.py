from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import edc_phq9_admin

app_name = "edc_phq9"

urlpatterns = [
    path("admin/", edc_phq9_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
