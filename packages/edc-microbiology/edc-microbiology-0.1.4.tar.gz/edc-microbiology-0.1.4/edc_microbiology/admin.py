from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from .admin_site import edc_microbiology_admin
from .forms import MicrobiologyForm
from .modeladmin_mixins import MicrobiologyModelAdminMixin
from .models import Microbiology


@admin.register(Microbiology, site=edc_microbiology_admin)
class MicrobiologyAdmin(
    MicrobiologyModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):
    form = MicrobiologyForm
