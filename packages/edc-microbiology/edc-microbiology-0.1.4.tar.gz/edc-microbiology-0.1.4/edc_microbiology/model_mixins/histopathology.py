from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import OtherCharField
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import BIOPSY_RESULTS_ORGANISM, CULTURE_RESULTS


class HistopathologyModelMixin(models.Model):

    tissue_biopsy_performed = models.CharField(
        verbose_name="Was a tissue biopsy taken", max_length=5, choices=YES_NO
    )

    tissue_biopsy_result = models.CharField(
        verbose_name="Tissue biopsy results",
        max_length=10,
        choices=CULTURE_RESULTS,
        default=NOT_APPLICABLE,
    )

    tissue_biopsy_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    tissue_biopsy_day = models.IntegerField(
        verbose_name="If POSITIVE, `study day` positive tissue biospy sample taken",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    tissue_biopsy_organism = models.CharField(
        verbose_name="If growth POSITIVE, organism",
        max_length=50,
        choices=BIOPSY_RESULTS_ORGANISM,
        default=NOT_APPLICABLE,
    )

    tissue_biopsy_organism_other = OtherCharField(max_length=50, null=True, blank=True)

    tissue_biopsy_organism_text = models.TextField(
        verbose_name="If growth positive, organism", null=True, blank=True
    )

    tissue_biopsy_report = models.TextField(
        verbose_name="Histopathoplogy report", null=True, blank=True
    )

    class Meta:
        abstract = True
