from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import edc_microbiology_admin

app_name = "edc_microbiology"

urlpatterns = [
    path("admin/", edc_microbiology_admin.urls),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
