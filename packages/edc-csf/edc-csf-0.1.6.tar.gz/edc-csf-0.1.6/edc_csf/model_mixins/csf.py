from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import (
    HIGH_LOW_NA,
    POS_NEG_NOT_DONE_NA,
    YES_NO_AWAITING_RESULTS,
    YES_NO_NA,
)
from edc_constants.constants import AWAITING_RESULTS, NOT_APPLICABLE


class CsfModelMixin(models.Model):

    csf_positive = models.CharField(
        verbose_name="CSF positive for cryptococcal meningitis?",
        max_length=18,
        choices=YES_NO_AWAITING_RESULTS,
        default=AWAITING_RESULTS,
    )

    india_ink = models.CharField(
        max_length=15, choices=POS_NEG_NOT_DONE_NA, default=NOT_APPLICABLE
    )

    csf_crag_lfa = models.CharField(
        verbose_name="CrAg LFA",
        max_length=15,
        choices=POS_NEG_NOT_DONE_NA,
        default=NOT_APPLICABLE,
    )

    sq_crag = models.CharField(
        verbose_name="SQ CrAg",
        max_length=15,
        choices=POS_NEG_NOT_DONE_NA,
        default=NOT_APPLICABLE,
    )

    sq_crag_pos = models.CharField(
        verbose_name="SQ CrAg",
        max_length=15,
        choices=HIGH_LOW_NA,
        default=NOT_APPLICABLE,
    )

    crf_crag_titre_done = models.CharField(
        verbose_name="Was the CRF CrAg titre done",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )
    crf_crag_titre = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
