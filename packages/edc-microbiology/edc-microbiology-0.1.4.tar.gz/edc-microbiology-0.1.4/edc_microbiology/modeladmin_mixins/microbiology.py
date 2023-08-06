from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple

from ..fieldsets import (
    get_sputum_afb_fieldset,
    get_sputum_culture_fieldset,
    get_sputum_genexpert_fieldset,
    get_urinary_lam_fieldset,
    get_urine_culture_fieldset,
)


class MicrobiologyModelAdminMixin:

    fieldsets = (
        get_urinary_lam_fieldset(),
        get_sputum_genexpert_fieldset(),
        get_sputum_culture_fieldset(),
        get_sputum_afb_fieldset(),
        get_urine_culture_fieldset(),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "sputum_afb_performed": admin.VERTICAL,
        "sputum_afb_result": admin.VERTICAL,
        "sputum_culture_performed": admin.VERTICAL,
        "sputum_culture_result": admin.VERTICAL,
        "sputum_genexpert_result": admin.VERTICAL,
        "sputum_genexpert_performed": admin.VERTICAL,
        "urinary_lam_performed": admin.VERTICAL,
        "urinary_lam_result": admin.VERTICAL,
        "urinary_lam_result_grade": admin.VERTICAL,
    }
