from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple

from ..fieldsets import get_histopathology_fieldset


class HistopathologyModelAdminMixin:

    fieldsets = (
        get_histopathology_fieldset(),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "tissue_biopsy_performed": admin.VERTICAL,
        "tissue_biopsy_result": admin.VERTICAL,
        "tissue_biopsy_organism": admin.VERTICAL,
    }
