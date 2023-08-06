from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from .form_validator import MnsiFormValidator
from .models import Mnsi


class MnsiForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = MnsiFormValidator

    class Meta:
        model = Mnsi
        fields = "__all__"
