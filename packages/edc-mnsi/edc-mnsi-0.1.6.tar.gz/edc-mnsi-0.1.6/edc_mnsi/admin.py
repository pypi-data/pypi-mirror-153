from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_list_data.admin import ListModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from edc_mnsi.fieldsets import calculated_values_fieldset
from edc_mnsi.fieldsets import get_fieldsets as get_mnsi_fieldsets
from edc_mnsi.model_admin_mixin import MnsiModelAdminMixin
from edc_mnsi.models import AbnormalFootAppearanceObservations

from .admin_site import edc_mnsi_admin
from .forms import MnsiForm
from .models import Mnsi


def get_fieldsets():
    fieldset = (
        None,
        {
            "fields": (
                "subject_identifier",
                "report_datetime",
                "mnsi_performed",
                "mnsi_not_performed_reason",
            )
        },
    )

    fieldsets = (fieldset,) + get_mnsi_fieldsets()
    fieldsets += (calculated_values_fieldset,)
    fieldsets += (audit_fieldset_tuple,)
    return fieldsets


@admin.register(AbnormalFootAppearanceObservations, site=edc_mnsi_admin)
class AbnormalFootAppearanceObservationsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Mnsi, site=edc_mnsi_admin)
class MnsiAdmin(
    MnsiModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = MnsiForm

    fieldsets = get_fieldsets()
