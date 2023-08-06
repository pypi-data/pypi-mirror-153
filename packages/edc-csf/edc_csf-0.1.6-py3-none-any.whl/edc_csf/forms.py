from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from .form_validators import LpCsfFormValidator
from .models import LpCsf


class LpCsfForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = LpCsfFormValidator

    class Meta:
        model = LpCsf
        fields = "__all__"
