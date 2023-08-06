from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import format_html
from edc_constants.choices import (
    POS_NEG,
    YES_NO_NA,
    YES_NO_NOT_DONE_AWAITING_RESULTS_NA,
)
from edc_constants.constants import AWAITING_RESULTS, NOT_APPLICABLE
from edc_model.validators import datetime_not_future
from edc_reportable import (
    GRAMS_PER_LITER,
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MM3_DISPLAY,
)

from ..choices import MG_MMOL_UNITS, MM3_PERC_UNITS


class CsfCultureModelMixin(models.Model):

    """add a requisition fields if needed, for example:

    csf_requisition = models.ForeignKey(
        get_requisition_model_name(),
        on_delete=PROTECT,
        related_name="csfrequisition",
        verbose_name="CSF Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit")
    """

    csf_culture_assay_datetime = models.DateTimeField(
        verbose_name="CSF Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    csf_culture = models.CharField(
        verbose_name="CSF Result: Other organism (non-Cryptococcus)",
        max_length=18,
        choices=YES_NO_NOT_DONE_AWAITING_RESULTS_NA,
        default=AWAITING_RESULTS,
        help_text="Complete after getting the results.",
    )

    other_csf_culture = models.CharField(
        verbose_name="If YES, specify organism:", max_length=75, blank=True, null=True
    )

    csf_wbc_cell_count = models.IntegerField(
        verbose_name="Total CSF WBC cell count:",
        help_text=format_html(f"acceptable units are {MM3_DISPLAY}"),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    differential_lymphocyte_count = models.IntegerField(
        verbose_name="Differential lymphocyte cell count:",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text=format_html(f"acceptable units are {MM3_DISPLAY} or %"),
    )

    differential_lymphocyte_unit = models.CharField(
        choices=MM3_PERC_UNITS, max_length=6, null=True, blank=True
    )

    differential_neutrophil_count = models.IntegerField(
        verbose_name="Differential neutrophil cell count:",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text=format_html(f"acceptable units are {MM3_DISPLAY} or %"),
    )

    differential_neutrophil_unit = models.CharField(
        choices=MM3_PERC_UNITS, max_length=6, null=True, blank=True
    )

    csf_glucose = models.DecimalField(
        verbose_name="CSF glucose:",
        decimal_places=1,
        max_digits=3,
        blank=True,
        null=True,
        help_text=f"Units in {MILLIMOLES_PER_LITER} or {MILLIGRAMS_PER_DECILITER}",
    )

    csf_glucose_units = models.CharField(
        verbose_name="CSF glucose units:",
        max_length=6,
        choices=MG_MMOL_UNITS,
        blank=True,
        null=True,
    )

    csf_protein = models.DecimalField(
        verbose_name="CSF protein:",
        decimal_places=2,
        max_digits=4,
        blank=True,
        null=True,
        help_text=f"Units in {GRAMS_PER_LITER}",
    )

    csf_crag = models.CharField(
        verbose_name="CSF CrAg:", max_length=15, choices=POS_NEG, blank=True, null=True
    )

    csf_crag_immy_lfa = models.CharField(
        verbose_name="CSF CrAg done by IMMY CrAg LFA:",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
