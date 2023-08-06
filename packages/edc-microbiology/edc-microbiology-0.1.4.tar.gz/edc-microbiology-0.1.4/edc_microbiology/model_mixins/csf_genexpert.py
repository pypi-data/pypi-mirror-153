from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import SPUTUM_GENEXPERT


class CsfGeneXpertModelMixin(models.Model):
    csf_genexpert_performed = models.CharField(
        verbose_name="CSF Gene-Xpert performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    csf_genexpert_date = models.DateField(
        verbose_name="Date CSF Gene-Xpert taken",
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True,
    )

    csf_genexpert_result = models.CharField(
        verbose_name="CSF Gene-Xpert results",
        max_length=45,
        choices=SPUTUM_GENEXPERT,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
