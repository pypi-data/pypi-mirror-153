from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple

from ..fieldsets import get_blood_culture_fieldset


class BloodCultureModelAdminMixin:

    fieldsets = (
        get_blood_culture_fieldset(),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "blood_culture_performed": admin.VERTICAL,
        "blood_culture_result": admin.VERTICAL,
        "blood_culture_organism": admin.VERTICAL,
        "blood_culture_bacteria": admin.VERTICAL,
    }
