from django.apps import apps as django_apps
from django.conf import settings
from django.db import models

# don't delete. so attr is searchable
EDC_MNSI_MODEL = "EDC_MNSI_MODEL"


def get_mnsi_model_name() -> str:
    return getattr(settings, EDC_MNSI_MODEL, "edc_mnsi.mnsi")


def get_mnsi_model_cls() -> models.Model:
    return django_apps.get_model(get_mnsi_model_name())
