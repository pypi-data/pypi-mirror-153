from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from ..model_mixins import MnsiModelMixin


class Mnsi(
    UniqueSubjectIdentifierFieldMixin,
    MnsiModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):

    report_datetime = models.DateTimeField(default=get_utcnow)

    on_site = CurrentSiteManager()
    objects = models.Manager()
    history = HistoricalRecords()

    class Meta(MnsiModelMixin.Meta, BaseUuidModel.Meta):
        pass
