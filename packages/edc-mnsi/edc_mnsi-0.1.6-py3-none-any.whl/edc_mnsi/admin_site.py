from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

edc_mnsi_admin = EdcAdminSite(name="edc_mnsi_admin", app_label=AppConfig.name)
