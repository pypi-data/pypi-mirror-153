from edc_auth.site_auths import site_auths

from .auth_objects import (
    EDC_MICROBIOLOGY,
    EDC_MICROBIOLOGY_SUPER,
    EDC_MICROBIOLOGY_VIEW,
    codenames,
)

site_auths.add_group(*codenames, name=EDC_MICROBIOLOGY_VIEW, view_only=True)
site_auths.add_group(*codenames, name=EDC_MICROBIOLOGY, no_delete=True)
site_auths.add_group(*codenames, name=EDC_MICROBIOLOGY_SUPER)
