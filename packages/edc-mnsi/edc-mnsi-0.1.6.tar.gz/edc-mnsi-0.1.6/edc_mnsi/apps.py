from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "edc_mnsi"
    verbose_name = "Edc MNSI"
    has_exportable_data = True
    include_in_administration_section = True
