from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from .form_validators import MicrobiologyFormValidator
from .models import Microbiology


class MicrobiologyForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = MicrobiologyFormValidator

    class Meta:
        model = Microbiology
        fields = "__all__"
