from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import edc_csf_admin

app_name = "edc_csf"

urlpatterns = [
    path("admin/", edc_csf_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
