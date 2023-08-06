from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import SPUTUM_CULTURE


class SputumCultureModelMixin(models.Model):

    sputum_culture_performed = models.CharField(
        verbose_name="Sputum culture performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sputum_culture_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    sputum_culture_result = models.CharField(
        verbose_name="Sputum culture results",
        max_length=10,
        choices=SPUTUM_CULTURE,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
