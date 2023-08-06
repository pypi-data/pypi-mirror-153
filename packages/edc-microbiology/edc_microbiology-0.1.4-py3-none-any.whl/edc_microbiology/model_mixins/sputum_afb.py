from django.db import models
from edc_constants.choices import POS_NEG_NA, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start


class SputumAfbModelMixin(models.Model):

    sputum_afb_performed = models.CharField(
        verbose_name="Sputum AFB microscopy performed?",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sputum_afb_date = models.DateField(
        verbose_name="Sputum AFB date",
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True,
    )

    sputum_afb_result = models.CharField(
        verbose_name="Sputum AFB results",
        max_length=10,
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
