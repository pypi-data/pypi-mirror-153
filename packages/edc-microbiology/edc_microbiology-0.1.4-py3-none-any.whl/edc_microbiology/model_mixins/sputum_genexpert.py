from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import SPUTUM_GENEXPERT


class SputumGenexpertModelMixin(models.Model):

    sputum_genexpert_performed = models.CharField(
        verbose_name="Sputum Gene-Xpert performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sputum_genexpert_date = models.DateField(
        verbose_name="Sputum Gene-Xpert date",
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True,
    )

    sputum_genexpert_result = models.CharField(
        verbose_name="Sputum Gene-Xpert results",
        max_length=45,
        choices=SPUTUM_GENEXPERT,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
