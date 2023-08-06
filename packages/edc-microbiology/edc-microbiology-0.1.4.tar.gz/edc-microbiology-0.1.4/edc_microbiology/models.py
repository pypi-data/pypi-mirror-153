from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from .model_mixins import (
    BloodCultureModelMixin,
    HistopathologyModelMixin,
    SputumAfbModelMixin,
    SputumCultureModelMixin,
    SputumGenexpertModelMixin,
    UrinaryLamModelMixin,
    UrineCultureModelMixin,
)


class Microbiology(
    UniqueSubjectIdentifierFieldMixin,
    UrinaryLamModelMixin,
    SputumGenexpertModelMixin,
    SputumCultureModelMixin,
    SputumAfbModelMixin,
    UrineCultureModelMixin,
    BloodCultureModelMixin,
    HistopathologyModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):

    report_datetime = models.DateTimeField(default=get_utcnow)

    on_site = CurrentSiteManager()
    objects = models.Manager()
    history = HistoricalRecords()

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Microbiology"
        verbose_name_plural = "Microbiology"
