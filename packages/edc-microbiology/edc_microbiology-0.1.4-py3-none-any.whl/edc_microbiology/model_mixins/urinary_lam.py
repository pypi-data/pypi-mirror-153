from django.db import models
from edc_constants.choices import POS_NEG_NA, YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model.validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import LAM_POS_RESULT


class UrinaryLamModelMixin(models.Model):

    urinary_lam_performed = models.CharField(
        verbose_name="Urinary LAM performed?",
        max_length=15,
        choices=YES_NO,
    )

    urinary_lam_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    urinary_lam_result = models.CharField(
        verbose_name="Urinary LAM result",
        max_length=25,
        choices=POS_NEG_NA,
    )

    urinary_lam_result_grade = models.CharField(
        verbose_name="If Urinary LAM is positive, grade",
        max_length=25,
        choices=LAM_POS_RESULT,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
