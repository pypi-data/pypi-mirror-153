from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import OtherCharField
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import CULTURE_RESULTS, URINE_CULTURE_RESULTS_ORGANISM


class UrineCultureModelMixin(models.Model):

    urine_culture_performed = models.CharField(
        max_length=5,
        choices=YES_NO,
        help_text="only for patients with >50 white cells in urine",
    )

    urine_culture_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    urine_culture_result = models.CharField(
        verbose_name="Urine culture results, if completed",
        max_length=10,
        choices=CULTURE_RESULTS,
        default=NOT_APPLICABLE,
    )

    urine_culture_organism = models.CharField(
        verbose_name="If positive, organism",
        max_length=25,
        choices=URINE_CULTURE_RESULTS_ORGANISM,
        default=NOT_APPLICABLE,
    )

    urine_culture_organism_other = OtherCharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True
