from typing import Any

from django import forms
from edc_constants.constants import NOT_DONE, YES
from edc_form_validators import REQUIRED_ERROR, FormValidator
from edc_lab import CrfRequisitionFormValidatorMixin
from edc_visit_schedule.constants import DAY1

from .panels import csf_chemistry_panel, csf_panel


def validate_percentage(cleaned_data: dict, field: str, unit: str):
    if cleaned_data.get(field):
        if cleaned_data.get(unit) == "%" and cleaned_data.get(field) > 100:
            raise forms.ValidationError({field: "Cannot be greater than 100%."})


class LpFormValidatorMixin:
    def validate_lp(self: Any):
        self.required_if(
            YES, field="opening_pressure_measured", field_required="opening_pressure"
        )
        opening_pressure = self.cleaned_data.get("opening_pressure")
        closing_pressure = self.cleaned_data.get("closing_pressure")
        try:
            if opening_pressure <= closing_pressure:
                raise forms.ValidationError(
                    {"closing_pressure": "Cannot be greater than the opening pressure."}
                )
        except TypeError:
            pass


class CsfCultureFormValidatorMixin:
    def validate_csf_culture(self: Any):
        self.required_if(YES, field="csf_culture", field_required="other_csf_culture")

        self.require_together(
            field="csf_requisition",
            field_required="csf_assay_datetime",
        )

        self.validate_requisition("csf_requisition", "csf_assay_datetime", csf_chemistry_panel)

        self.require_together(
            field="differential_lymphocyte_count",
            field_required="differential_lymphocyte_unit",
        )

        validate_percentage(
            self.cleaned_data,
            field="differential_lymphocyte_count",
            unit="differential_lymphocyte_unit",
        )

        self.require_together(
            field="differential_neutrophil_count",
            field_required="differential_neutrophil_unit",
        )

        validate_percentage(
            self.cleaned_data,
            field="differential_neutrophil_count",
            unit="differential_neutrophil_unit",
        )

        # csf_glucose
        self.require_together(field="csf_glucose", field_required="csf_glucose_units")

        # csf_crag
        self.not_required_if(NOT_DONE, field="csf_crag", field_required="csf_crag_lfa")

        # csf_cr_ag and india_ink
        if (
            self.cleaned_data.get("subject_visit").visit_code == DAY1
            and self.cleaned_data.get("subject_visit").visit_code_sequence == 0
        ):
            if (
                self.cleaned_data.get("csf_crag") == NOT_DONE
                and self.cleaned_data.get("india_ink") == NOT_DONE
            ):
                error_msg = 'CSF CrAg and India Ink cannot both be "not done".'
                message = {"csf_crag": error_msg, "india_ink": error_msg}
                raise forms.ValidationError(message, code=REQUIRED_ERROR)


class QuantitativeCsfFormValidatorMixin:
    def validate_quantitative_culture(self: Any, requisition: str):
        self.require_together(
            field=requisition,
            field_required="qc_assay_datetime",
        )
        self.validate_requisition(requisition, "qc_assay_datetime", csf_panel)
        self.required_if_true(
            self.cleaned_data.get("quantitative_culture") is not None,
            field_required=requisition,
        )


class BiosynexSemiQuantitativeCragMixinFormValidatorMixin:
    def validate_biosynex_semi_quantitative_crag(self: Any):
        self.applicable_if(YES, field="bios_crag", field_applicable="crag_control_result")

        self.applicable_if(YES, field="bios_crag", field_applicable="crag_t1_result")

        self.applicable_if(YES, field="bios_crag", field_applicable="crag_t2_result")


class LpCsfFormValidatorMixin(
    CrfRequisitionFormValidatorMixin,
    LpFormValidatorMixin,
    QuantitativeCsfFormValidatorMixin,
):

    requisition_fields = [
        ("qc_requisition", "qc_assay_datetime"),
        ("csf_requisition", "csf_assay_datetime"),
    ]

    def clean(self):

        self.validate_lp()

        self.validate_quantitative_culture("qc_requisition")


class LpCsfFormValidator(LpCsfFormValidatorMixin, FormValidator):

    pass
