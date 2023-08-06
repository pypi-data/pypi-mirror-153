from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import edc_mnsi_admin

app_name = "edc_mnsi"

urlpatterns = [
    path("admin/", edc_mnsi_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
